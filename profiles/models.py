from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills_offered = models.CharField(max_length=255, blank=True)
    skills_wanted = models.CharField(max_length=255, blank=True)
    skill_level = models.CharField(max_length=50, blank=True)
    availability = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.png')


    def __str__(self):
        return self.user.username
