from django.db import models
from core_api.models import User

class Faculty(models.Model):
    """
    Faculty model linked to the User model with additional profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # One-to-one relationship with User
    profile_pic = models.ImageField(
        upload_to='faculty_profiles',  # Directory for storing faculty profile pictures
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically add creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Automatically add update timestamp

    def __str__(self):
        return self.user.username  # Display username in admin panel and logs
