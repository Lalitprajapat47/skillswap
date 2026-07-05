from django.urls import path
from .views import profile_page, dashboard_view, edit_profile

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("edit/", edit_profile, name="edit_profile"),

    # profile page (logged-in user's own profile)
    path("my/", profile_page, name="profile"),

    # profile of other user by ID
    path("view/<int:user_id>/", profile_page, name="view_profile"),
]
