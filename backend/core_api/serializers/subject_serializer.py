from rest_framework import serializers
from core_api.serializers.faculty_serializer import FacultySerializer
from core_api.models.subject import Subject

class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subject model.
    This serializer includes:
    - Nested faculty details using the FacultySerializer.
    """
    # Nested serializer for associated Faculty object
    faculty = FacultySerializer()

    class Meta:
        """
        Meta class to define the model and fields for serialization.
        """
        model = Subject  # The model being serialized
        fields = ['id', 'name', 'faculty']  # Fields to include in the serialized output

    def update(self, instance, validated_data):
        """
        Update an existing Subject instance, including the associated Faculty object.
        """
        # Extract nested faculty data if provided
        faculty_data = validated_data.pop('faculty', None)

        # Update the associated Faculty object if faculty data is provided
        if faculty_data:
            faculty = instance.faculty  # Access the related Faculty instance
            for attr, value in faculty_data.items():
                # Update the fields of the associated Faculty's User object
                setattr(faculty.user, attr, value)
            faculty.user.save()  # Save the changes to the User instance

        # Update fields of the Subject instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the updated Subject instance
        instance.save()
        return instance
