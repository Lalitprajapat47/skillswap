from django.urls import path
from . import views

urlpatterns = [
    path("exchange/", views.skill_exchange_view, name="skill_exchange"),

    path("requests/", views.swap_requests, name="swap_requests"),
    path("send/<int:user_id>/", views.send_swap_request, name="send_swap_request"),
    path("handle/<int:request_id>/<str:action>/", views.handle_request, name="handle_swap_request"),

    # ✅ Learning Sessions
    path("sessions/", views.sessions_list, name="learning_sessions"),
    path("sessions/<int:session_id>/complete/", views.complete_session, name="complete_session"),

    path('sessions/<int:session_id>/review/', views.write_review, name='write_review'),
    path("sessions/<int:session_id>/chat/", views.session_chat, name="session_chat"),


]
