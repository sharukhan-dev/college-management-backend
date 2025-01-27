from rest_framework import viewsets
from rest_framework.response import Response
from core_api.models.subject import Subject
from core_api.models.student import Student
from core_api.serializers.subject_serializer import SubjectSerializer
from core_api.serializers.student_serializer import StudentSerializer
from core_api.serializers.faculty_serializer import FacultySerializer

class SubjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Subject operations.
    Provides CRUD operations for subjects and additional methods 
    for fetching enrolled students and assigned faculty.
    """
    queryset = Subject.objects.all()  # Default queryset for retrieving all subjects
    serializer_class = SubjectSerializer  # Serializer used for subject data

    def get_enrolled_students(self, request, pk=None):
        """
        Retrieve a list of students enrolled in a specific subject.

        Args:
            request: The HTTP request object.
            pk (int): Primary key of the subject.

        Returns:
            Response: A serialized list of students enrolled in the subject.
        """
        subject = self.get_object()  # Get the subject instance using the primary key
        students = Student.objects.filter(enrolled_subjects=subject)  # Fetch students enrolled in this subject
        serializer = StudentSerializer(students, many=True)  # Serialize the student data
        return Response(serializer.data)  # Return the serialized data as a response

    def get_teaching_faculty(self, request, pk=None):
        """
        Retrieve the faculty teaching a specific subject.

        Args:
            request: The HTTP request object.
            pk (int): Primary key of the subject.

        Returns:
            Response: Serialized data of the faculty teaching the subject or an error message.
        """
        try:
            subject = self.get_object()  # Retrieve the subject instance by its primary key

            # Check if the subject has an assigned faculty
            if not subject.faculty:
                return Response({'error': 'No faculty assigned to this subject.'}, status=404)

            serializer = FacultySerializer(subject.faculty)  # Serialize the faculty data
            return Response(serializer.data, status=200)  # Return the serialized faculty data
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found.'}, status=404)  # Error response if subject is not found
        except Exception as e:
            # Log the unexpected error for debugging
            print(f"Unexpected error while fetching faculty for subject {pk}: {str(e)}")
            return Response({'error': 'An unexpected error occurred.'}, status=500)
