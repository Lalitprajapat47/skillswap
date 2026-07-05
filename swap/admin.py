from django.contrib import admin
from .models import SwapRequest
from .models import LearningSession
from .models import Review

admin.site.register(Review)


admin.site.register(LearningSession)

@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("sender__username", "receiver__username")
