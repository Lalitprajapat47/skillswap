from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from swap.models import SwapRequest
from .utils import get_user_badge


# =============  PROFILE VIEW  =================
@login_required
def profile_page(request, user_id=None):
    """
    If user_id is provided → view someone else's profile
    If not → view own profile
    """

    # own profile
    if user_id is None:
        profile = get_object_or_404(UserProfile, user=request.user)
        profile_user = request.user
    else:
        profile_user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(UserProfile, user=profile_user)

    # skills
    skills_offered = profile.skills_offered.split(",") if profile.skills_offered else []
    skills_wanted = profile.skills_wanted.split(",") if profile.skills_wanted else []

    # badge + trust score
    badge_info = get_user_badge(profile_user)

    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "profile_user": profile_user,
            "skills_offered": skills_offered,
            "skills_wanted": skills_wanted,
            "badge_info": badge_info,
        },
    )


# ============= EDIT PROFILE ==============
@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        profile.bio = request.POST.get("bio")
        profile.skills_offered = request.POST.get("skills_offered")
        profile.skills_wanted = request.POST.get("skills_wanted")
        profile.skill_level = request.POST.get("skill_level")
        profile.availability = request.POST.get("availability")

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES.get("profile_image")

        profile.save()
        return redirect("profile")

    return render(request, "edit_profile.html", {"profile": profile})


# ============= DASHBOARD VIEW ==============
@login_required
def dashboard_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    incoming_count = SwapRequest.objects.filter(receiver=request.user).count()
    outgoing_count = SwapRequest.objects.filter(sender=request.user).count()
    completed_count = SwapRequest.objects.filter(
        status="Accepted", sender=request.user
    ).count()

    profile_completion = calculate_profile_completion(profile)

    weekly_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekly_data = [1, 2, 0, 3, 1, 0, 2]

    recent_activity = [
        {"title": "Sent a swap request", "time": "2 hours ago"},
        {"title": "Updated profile", "time": "Yesterday"},
        {"title": "Completed a session", "time": "3 days ago"},
    ]

    return render(
        request,
        "dashboard.html",
        {
            "incoming_count": incoming_count,
            "outgoing_count": outgoing_count,
            "completed_count": completed_count,
            "profile_completion": profile_completion,
            "weekly_labels": weekly_labels,
            "weekly_data": weekly_data,
            "recent_activity": recent_activity,
        },
    )


# ========== PROFILE COMPLETION FUNCTION ============
def calculate_profile_completion(profile):
    completion = 0
    fields = [
        profile.bio,
        profile.skills_offered,
        profile.skills_wanted,
        profile.skill_level,
        profile.availability,
        profile.profile_image,
    ]
    for f in fields:
        if f:
            completion += 100 / len(fields)
    return int(completion)
