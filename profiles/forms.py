from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "bio",
            "skills_offered",
            "skills_wanted",
            "skill_level",
            "availability"
        ]

        widgets = {
            "skills_offered": forms.TextInput(attrs={"placeholder": "I can teach..."}),
            "skills_wanted": forms.TextInput(attrs={"placeholder": "I want to learn..."}),
            "skill_level": forms.TextInput(attrs={"placeholder": "Beginner / Intermediate / Expert"}),
            "availability": forms.TextInput(attrs={"placeholder": "e.g. 6–9 PM"}),
        }
