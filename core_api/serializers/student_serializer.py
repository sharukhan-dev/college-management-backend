from rest_framework import serializers
from core_api.models.faculty import Faculty
from core_api.serializers.user_serializer import UserSerializer
from core_api.serializers.subject_serializer import SubjectSerializer
from core_api.models.student import Student
from core_api.models.subject import Subject
from core_api.models.user import User
from django.utils.timezone import now

class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.
    This serializer includes:
    - Nested user details using the UserSerializer.
    - List of enrolled subjects using the SubjectSerializer.
    """
    # Nested serializer for associated User object
    user = UserSerializer()
    # Many-to-many relationship field for enrolled subjects
    enrolled_subjects = SubjectSerializer(many=True, required=False)  

    class Meta:
        """
        Meta class to define the model, included fields, and extra configurations.
        """
        model = Student
        fields = [
            'user', 'profile_pic', 'first_name', 'last_name',
            'date_of_birth', 'gender', 'blood_group',
            'contact_number', 'address', 'enrolled_subjects'
        ]
        # Additional keyword arguments for specific fields
        extra_kwargs = {
            'profile_pic': {'required': False},
            'enrolled_subjects': {'required': False},
        }

    def create(self, validated_data):
        """
        Create a new Student instance, along with the associated User object.
        """
        # Extract nested user data
        user_data = validated_data.pop('user')
        # Access the request object from the serializer context
        request = self.context['request']

        # Create the User object for the student
        user = User.objects.create_user(
            username=user_data['username'],  # Set username
            password=user_data['password'],  # Set password
            email=user_data.get('email', ''),  # Set email, default to empty string
            user_type=2  # User type 2 represents a Student
        )

        # Handle profile picture if provided in the request
        profile_pic = request.FILES.get('profile_pic', None)

        # Create the Student object
        student = Student.objects.create(user=user, profile_pic=profile_pic, **validated_data)

        # Automatically enroll the student in the faculty's subject if the request is made by a faculty member
        if request.user.user_type == 1:  # Check if the requester is a faculty member
            faculty = Faculty.objects.get(user=request.user)  # Get the faculty instance
            if faculty.teaching_subject:  # Check if the faculty has a subject
                student.enrolled_subjects.add(faculty.teaching_subject)  # Add the subject to the student's enrolled subjects
        return student

    def update(self, instance, validated_data):
        """
        Update an existing Student instance, including the associated User object.
        """
        # Extract nested user data if provided
        user_data = validated_data.pop('user', None)

        # Update the associated User object
        if user_data:
            user = instance.user  # Access the related User instance
            user.username = user_data.get('username', user.username)  # Update username if provided
            user.email = user_data.get('email', user.email)  # Update email if provided
            if 'password' in user_data:  # Update password if provided
                user.set_password(user_data['password'])
            user.save()  # Save the changes to the User instance

        # Update fields of the Student instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle profile picture updates explicitly
        profile_pic = self.context['request'].FILES.get('profile_pic', None)
        if profile_pic:  # Update the profile picture if provided
            instance.profile_pic = profile_pic
        elif 'profile_pic' in validated_data:  # Clear the profile picture if null is passed
            instance.profile_pic = None

        # Save the updated Student instance
        instance.save()
        return instance
