from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def call_room(request, room_id):
    return render(request, "call_room.html", {
        "room_id": room_id,
        "call_type": request.GET.get("type", "video")
    })
