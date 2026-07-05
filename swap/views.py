from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import UserProfile
from .models import SwapRequest, LearningSession, Review
from django.db.models import Q
from chat.models import Message
# from reviews.models import Review


# ACCEPT REQUEST + AUTO CREATE SESSION
@login_required
def accept_request(request, req_id):
    swap_request = get_object_or_404(SwapRequest, id=req_id)

    swap_request.status = "Accepted"
    swap_request.save()

    # AUTO CREATE SESSION
    LearningSession.objects.create(
        sender=swap_request.sender,
        receiver=swap_request.receiver,
        topic=f"{swap_request.skill_from_sender} ↔ {swap_request.skill_from_receiver}",
        status="Ongoing",
    )

    return redirect("swap_requests")


# COMPLETE SESSION → GO TO REVIEW PAGE
@login_required
def complete_session(request, session_id):
    session = get_object_or_404(LearningSession, id=session_id)

    # safety: koi random user kisi aur ka session complete na kar de
    if session.sender != request.user and session.receiver != request.user:
        return redirect("learning_sessions")

    session.status = "Completed"
    session.save()

    # ab review ke page pe bhejenge
    return redirect("write_review", session_id=session.id)


# LIST OF ALL USERS WITH RATING
@login_required
def skill_exchange_view(request):
    profiles = UserProfile.objects.exclude(user=request.user)

    # ⭐ Add rating info for each user
    for p in profiles:
        all_reviews = p.user.received_reviews.all()

        if all_reviews.exists():
            avg_rating = sum(r.rating for r in all_reviews) / all_reviews.count()
            p.avg_rating = round(avg_rating, 1)
            p.stars = "★" * int(avg_rating)
        else:
            p.avg_rating = 0
            p.stars = ""
    
    return render(request, "skill_exchange.html", {"profiles": profiles})



# SEND SWAP REQUEST
@login_required
def send_swap_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    sender_profile = request.user.userprofile
    receiver_profile = receiver.userprofile

    sender_skill = sender_profile.skills_offered.split(",")[0].strip() if sender_profile.skills_offered else ""
    receiver_skill = receiver_profile.skills_offered.split(",")[0].strip() if receiver_profile.skills_offered else ""

    SwapRequest.objects.create(
        sender=request.user,
        receiver=receiver,
        skill_from_sender=sender_skill,
        skill_from_receiver=receiver_skill,
    )

    return redirect("swap_requests")


# INCOMING + OUTGOING REQUESTS
@login_required
def swap_requests(request):
    incoming = SwapRequest.objects.filter(
        receiver=request.user,
        status="Pending"
    )

    outgoing = SwapRequest.objects.filter(sender=request.user)

    return render(request, "swap_requests.html", {
        "incoming": incoming,
        "outgoing": outgoing,
    })


# HANDLE ACCEPT / REJECT BUTTONS
@login_required
def handle_request(request, request_id, action):
    swap_request = get_object_or_404(
        SwapRequest,
        id=request_id,
        receiver=request.user
    )

    if action == "accept":
        if swap_request.status != "Accepted":
            swap_request.status = "Accepted"
            swap_request.save()

            LearningSession.objects.get_or_create(
                sender=swap_request.sender,
                receiver=swap_request.receiver,
                topic=f"{swap_request.skill_from_sender} ↔ {swap_request.skill_from_receiver}",
                defaults={"status": "Ongoing"}
            )

    elif action == "reject":
        swap_request.status = "Rejected"
        swap_request.save()

    return redirect("swap_requests")


# WRITE REVIEW
def write_review(request, session_id):
    session = get_object_or_404(LearningSession, id=session_id)

    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        feedback = request.POST.get("feedback")

        review = Review.objects.create(
            session=session,
            reviewer=request.user,
            reviewed_user=session.receiver if request.user == session.sender else session.sender,
            rating=rating,
            feedback=feedback
        )

        session.review = review
        session.save()

        return redirect("learning_sessions")

    return render(request, "write_review.html", {"session": session})



# REJECT REQUEST
@login_required
def reject_request(request, request_id):
    req = get_object_or_404(SwapRequest, id=request_id, receiver=request.user)

    if request.method == "POST":
        req.status = "Rejected"
        req.save()

    return redirect("swap_requests")


# SESSION LIST PAGE
@login_required
def sessions_list(request):
    user_filter = Q(sender=request.user) | Q(receiver=request.user)

    ongoing_sessions = (
        LearningSession.objects
        .filter(user_filter, status="Ongoing")
        .order_by("-created_at")
    )

    completed_sessions = (
        LearningSession.objects
        .filter(user_filter, status="Completed")
        .order_by("-created_at")
    )

    context = {
        "ongoing_sessions": ongoing_sessions,
        "completed_sessions": completed_sessions,
    }
    return render(request, "learning_sessions.html", context)

from chat.models import Message

@login_required
def session_chat(request, session_id):
    session = get_object_or_404(LearningSession, id=session_id)

    if request.user not in [session.sender, session.receiver]:
        return redirect("learning_sessions")

    if request.method == "POST":
        text = request.POST.get("message")
        if text and text.strip():
            Message.objects.create(
                session=session,
                sender=request.user,
                content=text
            )
        return redirect("session_chat", session_id=session.id)

    messages = Message.objects.filter(session=session).order_by("timestamp")

    return render(request, "session_chat.html", {
        "session": session,
        "messages": messages
    })
