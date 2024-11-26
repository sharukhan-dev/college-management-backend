from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending AbstractUser to include a user_type field
    for differentiating between Faculty and Students.
    """
    USER_TYPE_CHOICES = (
        (1, 'Faculty'),  # Faculty user type
        (2, 'Student'),  # Student user type
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)  # Default to Student

    # Resolving conflicts with Django's default related names
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Unique related name for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Unique related name for permissions
        blank=True
    )
