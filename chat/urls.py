from django.urls import path
from . import views

urlpatterns = [
    path("session/<int:session_id>/", views.session_chat, name="session_chat"),
    path("upload/<int:session_id>/", views.upload_file, name="upload_file"),
]
