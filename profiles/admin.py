from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "skills_offered", "skills_wanted", "skill_level", "availability")
    search_fields = ("user__username", "skills_offered", "skills_wanted")
