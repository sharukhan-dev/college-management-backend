from rest_framework import serializers
from core_api.serializers.user_serializer import UserSerializer
from core_api.models.faculty import Faculty
from core_api.models.user import User

class FacultySerializer(serializers.ModelSerializer):
    """
    Serializer for the Faculty model.
    This serializer includes:
    - Nested user details using the UserSerializer.
    - Subject information via a StringRelatedField for better readability.
    """
    # Nested serializer for the associated User object
    user = UserSerializer()  
    # Field to display the teaching subject as a string (e.g., subject name)
    teaching_subject = serializers.StringRelatedField()  

    class Meta:
        """
        Meta class to define the model and fields included in the serializer.
        """
        model = Faculty
        # Fields to include in the serialized output
        fields = ['user', 'profile_pic', 'teaching_subject']

    def create(self, validated_data):
        """
        Create a new Faculty instance along with a related User instance.
        """
        # Extract nested user data from the validated data
        user_data = validated_data.pop('user')
        # Create a User instance with the extracted data
        user = User.objects.create_user(
            username=user_data['username'],  # Set username
            password=user_data['password'],  # Set password
            email=user_data.get('email', ''),  # Set email, default to empty string
            user_type=1  # User type 1 represents a Faculty
        )
        # Create a Faculty instance and associate it with the created User
        faculty = Faculty.objects.create(user=user, **validated_data)
        return faculty

    def update(self, instance, validated_data):
        """
        Update an existing Faculty instance, including its related User.
        """
        # Extract nested user data if provided
        user_data = validated_data.pop('user', None)

        # If user data is provided, update the User instance
        if user_data:
            user = instance.user
            # Update fields in the User instance
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        # Explicitly handle profile_pic updates if included in the request
        profile_pic = self.context['request'].FILES.get('profile_pic', None)
        if profile_pic:  # Update the profile picture if provided
            instance.profile_pic = profile_pic
        elif 'profile_pic' in validated_data:  # Clear the profile picture if null is passed
            instance.profile_pic = None

        # Update other fields of the Faculty instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
