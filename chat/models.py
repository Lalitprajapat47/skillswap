from django.db import models
from django.contrib.auth.models import User
from swap.models import LearningSession


class Message(models.Model):
    session = models.ForeignKey(
        LearningSession,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    # TEXT
    content = models.TextField(blank=True)

    # FILE
    attachment = models.FileField(
        upload_to="chat_attachments/",
        blank=True,
        null=True
    )

    is_image = models.BooleanField(default=False)

    # META
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20] or 'FILE'}"
