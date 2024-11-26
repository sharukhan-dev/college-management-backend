from django.db import models

class Subject(models.Model):
    """
    Subject model representing a single subject taught by a faculty member.
    """
    name = models.CharField(max_length=100)  # Name of the subject
    faculty = models.OneToOneField(
        'Faculty',  # One-to-one relationship with Faculty
        on_delete=models.CASCADE,  # Deleting a faculty deletes the subject
        related_name='teaching_subject'
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically add creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Automatically add update timestamp

    def __str__(self):
        return self.name  # Display subject name in admin panel and logs
