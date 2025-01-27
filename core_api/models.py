"""
Main models entry point for the application.

This file imports models from their respective modules for a modular and organized codebase.
"""

# Import models from separate files
from core_api.models.user import User  # Custom User model with user_type field
from core_api.models.faculty import Faculty  # Faculty model linked to User
from core_api.models.student import Student  # Student model linked to User
from core_api.models.subject import Subject  # Subject model linked to Faculty
