from profiles.models import UserProfile
from profiles.views import calculate_profile_completion


def calculate_match_score(user_profile, other_profile):
    """
    Smart match scoring system
    """

    score = 0

    # Convert skills to lists
    my_teach = [s.strip().lower() for s in (user_profile.skills_offered or "").split(",") if s.strip()]
    my_learn = [s.strip().lower() for s in (user_profile.skills_wanted or "").split(",") if s.strip()]

    their_teach = [s.strip().lower() for s in (other_profile.skills_offered or "").split(",") if s.strip()]
    their_learn = [s.strip().lower() for s in (other_profile.skills_wanted or "").split(",") if s.strip()]

    # 1. They teach what I want
    if set(my_learn) & set(their_teach):
        score += 60

    # 2. I teach what they want
    if set(my_teach) & set(their_learn):
        score += 40

    # 3. Add bonus for profile completion
    score += calculate_profile_completion(other_profile) / 10

    return score


def find_matches_for_user(user):
    """
    Returns sorted match list for dashboard
    """
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        return []

    matches = []

    for other in UserProfile.objects.exclude(user=user):
        score = calculate_match_score(user_profile, other)

        if score > 0:  # Only meaningful matches
            matches.append((other, score))

    # Sort highest score first
    matches = sorted(matches, key=lambda x: x[1], reverse=True)

    # Return only profiles (not scores)
    return [m[0] for m in matches]
