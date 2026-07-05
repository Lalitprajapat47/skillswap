from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    skill_tag = models.CharField(max_length=100, help_text="e.g. Python, Guitar, Cooking")

    file = models.FileField(upload_to='resources/', blank=True, null=True)
    link = models.URLField(blank=True)

    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_file(self):
        return bool(self.file)