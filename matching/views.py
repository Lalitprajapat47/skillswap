from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import find_matches_for_user
from profiles.models import UserProfile
from profiles.utils import get_user_badge


@login_required
def matches_view(request):
    matches = find_matches_for_user(request.user)
    return render(request, "matches.html", {"matches": matches})


@login_required
def search(request):
    want = request.GET.get("want")
    offer = request.GET.get("offer")

    results = []

    if want and offer:
        # Sahi match: doosra banda WO sikhaye jo main seekhna chahta hoon (want),
        # aur WO seekhna chahe jo main sikha sakta hoon (offer)
        profiles = UserProfile.objects.filter(
            skills_offered__icontains=want,
            skills_wanted__icontains=offer
        ).exclude(user=request.user)

        for p in profiles:
            badge_info = get_user_badge(p.user)
            results.append({
                "profile": p,
                "badge": badge_info,
            })

    return render(request, "search_results.html", {
        "results": results,
        "searched_want": want,
        "searched_offer": offer,
    })