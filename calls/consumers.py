import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

# {group_name: [channel_name, ...]}  -> pehla entry = caller, doosra = callee
call_rooms = {}


class CallConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.group_name = f"call_{self.room_id}"
        self.user = self.scope["user"]

        query = parse_qs(self.scope["query_string"].decode())
        self.call_type = query.get("type", ["audio"])[0]

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        members = call_rooms.setdefault(self.group_name, [])

        if not members:
            # Pehla banda -> ye "caller" hai
            members.append((self.channel_name, self.user.username))
            await self.send(text_data=json.dumps({
                "event": "role",
                "role": "caller",
                "you": self.user.username,
            }))

            # 🔔 Doosre banda ko POORI WEBSITE PE notify karo (jahan bhi wo ho)
            peer_id = await self.get_peer_id()
            if peer_id:
                await self.channel_layer.group_send(f"user_{peer_id}", {
                    "type": "notify_event",
                    "event": "call_invite",
                    "session_id": self.room_id,
                    "call_type": self.call_type,
                    "caller": self.user.username,
                })

        else:
            # Doosra banda -> ye "callee" hai
            caller_channel, caller_username = members[0]
            members.append((self.channel_name, self.user.username))

            await self.send(text_data=json.dumps({
                "event": "role",
                "role": "callee",
                "you": self.user.username,
                "peer": caller_username,
            }))

            await self.channel_layer.send(caller_channel, {
                "type": "call_event",
                "event": "peer_joined",
                "peer": self.user.username,
            })

    async def disconnect(self, code):
        members = call_rooms.get(self.group_name, [])
        was_solo_caller = len(members) == 1

        members[:] = [m for m in members if m[0] != self.channel_name]

        if not members:
            call_rooms.pop(self.group_name, None)

            # Agar caller akela wait kar raha tha (callee kabhi join hi nahi hua)
            # aur usne call cancel/end kar di, toh callee ka popup band karwao
            if was_solo_caller:
                peer_id = await self.get_peer_id()
                if peer_id:
                    await self.channel_layer.group_send(f"user_{peer_id}", {
                        "type": "notify_event",
                        "event": "call_cancelled",
                        "session_id": self.room_id,
                    })
        else:
            await self.channel_layer.group_send(self.group_name, {
                "type": "call_event",
                "event": "peer_left",
                "user": self.user.username,
            })

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        members = call_rooms.get(self.group_name, [])

        # Sirf DOOSRE banda ko bhejo — khud ko echo wapas NAHI aana chahiye,
        # warna offer/answer khud ko hi mil jaata hai aur RTCPeerConnection
        # ka state machine crash ho jaata hai ("wrong state" errors)
        for channel_name, _username in members:
            if channel_name != self.channel_name:
                await self.channel_layer.send(channel_name, {
                    "type": "call_event",
                    **data,
                })

    async def call_event(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_peer_id(self):
        from swap.models import LearningSession
        try:
            session = LearningSession.objects.get(id=self.room_id)
        except LearningSession.DoesNotExist:
            return None
        if session.sender_id == self.user.id:
            return session.receiver_id
        return session.sender_id


class NotifyConsumer(AsyncWebsocketConsumer):
    """
    Har page pe connected rehta hai (base.html se). Isi ke through
    incoming call ki notification poori website mein kahin bhi milegi,
    call-room page pe hone ki zaroorat nahi.
    """

    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notify_event(self, event):
        await self.send(text_data=json.dumps(event))