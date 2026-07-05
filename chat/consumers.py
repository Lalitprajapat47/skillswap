import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Message
from swap.models import LearningSession

# {room_name: {user_id: connection_count}}
online_rooms = {}


class SessionChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.room = f"chat_{self.session_id}"
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(self.room, self.channel_name)
        await self.accept()

        room_users = online_rooms.setdefault(self.room, {})
        room_users[self.user.id] = room_users.get(self.user.id, 0) + 1

        # tell everyone: "I (this user) am online"
        await self.channel_layer.group_send(
            self.room,
            {
                "type": "status_event",
                "event": "status",
                "user": self.user.username,
                "online": True,
            }
        )

        # tell MYSELF the current status of whoever else is already in the room
        # (so I see the correct status immediately on join, not just "offline" default)
        for uid, count in room_users.items():
            if uid != self.user.id and count > 0:
                peer_username = await self.get_username(uid)
                await self.send(text_data=json.dumps({
                    "type": "status_event",
                    "event": "status",
                    "user": peer_username,
                    "online": True,
                }))

    async def disconnect(self, close_code):
        room_users = online_rooms.get(self.room, {})
        if self.user.id in room_users:
            room_users[self.user.id] -= 1
            if room_users[self.user.id] <= 0:
                del room_users[self.user.id]

                # sirf tabhi "offline" bhejo jab is user ka koi bhi tab/connection na bacha ho
                await self.channel_layer.group_send(
                    self.room,
                    {
                        "type": "status_event",
                        "event": "status",
                        "user": self.user.username,
                        "online": False,
                    }
                )

        await self.channel_layer.group_discard(self.room, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        kind = data.get("kind")

        # -------- TEXT MESSAGE --------
        if kind == "chat":
            msg = await self.save_message(data.get("message", ""))

            await self.channel_layer.group_send(
                self.room,
                {
                    "type": "chat_event",
                    "event": "chat",
                    "sender": self.user.username,
                    "message": msg.content,
                    "time": timezone.localtime(msg.timestamp).strftime("%H:%M"),
                }
            )

        # -------- FILE MESSAGE --------
        elif kind == "file":
            await self.channel_layer.group_send(
                self.room,
                {
                    "type": "file_event",
                    "event": "file",
                    "sender": data["sender"],
                    "file_url": data["file_url"],
                    "is_image": data["is_image"],
                    "time": data["time"],
                }
            )

        # -------- READ RECEIPT --------
        elif kind == "read":
            await self.mark_seen()
            await self.channel_layer.group_send(
                self.room,
                {
                    "type": "read_event",
                    "event": "read",
                    "reader": self.user.username,
                }
            )

    # ================= EVENTS =================

    async def chat_event(self, event):
        await self.send(text_data=json.dumps(event))

    async def file_event(self, event):
        await self.send(text_data=json.dumps(event))

    async def read_event(self, event):
        await self.send(text_data=json.dumps(event))

    async def status_event(self, event):
        await self.send(text_data=json.dumps(event))

    # ================= DB =================

    @database_sync_to_async
    def save_message(self, text):
        session = LearningSession.objects.get(id=self.session_id)
        return Message.objects.create(
            session=session,
            sender=self.user,
            content=text,
        )

    @database_sync_to_async
    def mark_seen(self):
        Message.objects.filter(
            session_id=self.session_id,
            seen=False
        ).exclude(sender=self.user).update(
            seen=True
        )

    @database_sync_to_async
    def get_username(self, uid):
        return User.objects.get(id=uid).username