from rest_framework import serializers
from core_api.models.user import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Provides functionality for creating and updating User instances.
    Ensures sensitive data, such as passwords, remains secure.
    """

    class Meta:
        """
        Meta class to define the model and fields for serialization.
        """
        model = User  # Model to be serialized
        fields = ['id', 'username', 'password', 'email', 'user_type']  # Fields to include in serialized output
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure the password is only used during writes and not exposed in responses
        }

    def validate_username(self, value):
        """
        Validate that the username is unique.

        Args:
            value (str): The username to validate.

        Raises:
            serializers.ValidationError: If a user with the same username exists.

        Returns:
            str: The validated username.
        """
        if User.objects.filter(username=value).exists():  # Check for existing username
            raise serializers.ValidationError("A user with this username already exists.")  # Raise an error if duplicate
        return value

    def validate_email(self, value):
        """
        Validate that the email is unique.

        Args:
            value (str): The email to validate.

        Raises:
            serializers.ValidationError: If a user with the same email exists.

        Returns:
            str: The validated email.
        """
        if User.objects.filter(email=value).exists():  # Check for existing email
            raise serializers.ValidationError("A user with this email already exists.")  # Raise an error if duplicate
        return value
