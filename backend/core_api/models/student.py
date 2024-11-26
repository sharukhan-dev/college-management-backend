from django.db import models
from core_api.models import User, Faculty

class Student(models.Model):
    """
    Student model linked to the User model with additional details.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # One-to-one relationship with User
    profile_pic = models.ImageField(
        upload_to='student_profiles',  # Directory for storing student profile pictures
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=50)  # Student's first name
    last_name = models.CharField(max_length=50)  # Student's last name
    date_of_birth = models.DateField()  # Date of birth
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')]  # Gender options
    )
    blood_group = models.CharField(max_length=3)  # Blood group (e.g., A+, O-)
    contact_number = models.CharField(
        max_length=15,
        help_text="Enter a valid phone number (max 15 digits)."  # Add help text for clarity
    )
    address = models.TextField()  # Address
    enrolled_subjects = models.ManyToManyField(
        'Subject',  # Many-to-many relationship with Subject
        related_name='students',
        blank= True,
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically add creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Automatically add update timestamp

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Display full name
