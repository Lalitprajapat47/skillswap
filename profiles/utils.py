from django.db.models import Avg
from swap.models import Review

def get_user_badge(user):
    avg = Review.objects.filter(reviewed_user=user).aggregate(avg=Avg("rating"))["avg"]
    avg = round(avg, 1) if avg else 0

    trust_score = int((avg / 5) * 100)

    # Badge System
    if avg == 0:
        badge = "New Learner"
    elif trust_score <= 50:
        badge = "Reliable"
    elif trust_score <= 75:
        badge = "Trusted User"
    elif trust_score <= 90:
        badge = "Expert Mentor"
    else:
        badge = "Top Rated"

    # Auto stars: ⭐⭐⭐⭐✩
    stars = "⭐" * int(avg) + "✩" * (5 - int(avg))

    return {
        "avg": avg,
        "stars": stars,
        "trust_score": trust_score,
        "badge": badge,
    }
