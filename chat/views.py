from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone

from swap.models import LearningSession
from .models import Message


@login_required
def session_chat(request, session_id):
    session = get_object_or_404(LearningSession, id=session_id)

    messages = Message.objects.filter(
        session=session
    ).select_related("sender")

    return render(request, "session_chat.html", {
        "session": session,
        "messages": messages,
    })


@login_required
def upload_file(request, session_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    file = request.FILES.get("file")
    if not file:
        return JsonResponse({"error": "No file"}, status=400)

    session = LearningSession.objects.get(id=session_id)

    path = default_storage.save(
        f"chat_attachments/{file.name}",
        ContentFile(file.read())
    )

    message = Message.objects.create(
        session=session,
        sender=request.user,
        attachment=path,
        is_image=file.content_type.startswith("image/")
    )

    return JsonResponse({
        "id": message.id,
        "sender": request.user.username,
        "file_url": message.attachment.url,
        "is_image": message.is_image,
        "time": message.timestamp.strftime("%H:%M")
    })