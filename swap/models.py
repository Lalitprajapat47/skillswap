from django.db import models
from django.contrib.auth.models import User


class SwapRequest(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    )

    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)

    skill_from_sender = models.CharField(max_length=100)
    skill_from_receiver = models.CharField(max_length=100)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver}"


# -------------------------------------------------------
# 1️⃣ LearningSession ALWAYS comes BEFORE Review
# -------------------------------------------------------
class LearningSession(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_sessions")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_sessions")

    topic = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="Ongoing")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic} ({self.sender} ↔ {self.receiver})"


# -------------------------------------------------------
# 2️⃣ Review Model (Correct, NO CIRCULAR DEPENDENCY)
# -------------------------------------------------------
class Review(models.Model):

    # One review per session
    session = models.OneToOneField(
    LearningSession,
    on_delete=models.CASCADE,
    related_name="review",
    null=True,   # <-- ADD THIS TEMPORARILY
    blank=True
)


    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_reviews"
    )

    reviewed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_reviews"
    )

    rating = models.IntegerField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer}"
