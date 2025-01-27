import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from core_api.models.student import Student
from core_api.models.faculty import Faculty
from core_api.serializers.student_serializer import StudentSerializer
from core_api.serializers.subject_serializer import SubjectSerializer
import logging

logger = logging.getLogger(__name__)

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for student operations.
    Manages CRUD operations for students, ensuring faculty restrictions are respected.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Handles creating a new student instance.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Serialized student data or an error message.
        """
        try:
            # Parse student data from the request
            student_data = json.loads(request.data.get('student_data', '{}'))
            
            serializer = self.get_serializer(data=student_data)
            serializer.context['request'] = request
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating student: {e}")
            return Response({"error": "Failed to create student.", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        Handles updating a student's details.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Updated student data or an error message.
        """
        try:
            # Parse student data from the request
            student_data = json.loads(request.data.get('student_data', '{}'))
            instance = self.get_object()
            
            # Check if the logged-in faculty is authorized
            faculty = Faculty.objects.get(user=request.user)
            if not instance.enrolled_subjects.filter(faculty=faculty).exists():
                return Response({"error": "You are not authorized to update this student."},
                                status=status.HTTP_403_FORBIDDEN)

            # Perform the update operation
            serializer = self.get_serializer(instance, data=student_data, partial=True)
            serializer.context['request'] = request
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error updating student: {e}")
            return Response({"error": "Failed to update student.", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='me')
    def get_logged_in_student(self, request):
        """
        Fetch details of the currently logged-in student.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Serialized student data or an error message.
        """
        try:
            student = Student.objects.get(user=request.user)
            serializer = self.get_serializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='me/enrolled-subjects')
    def get_logged_in_student_subjects(self, request):
        """
        Fetch the subjects enrolled by the currently logged-in student.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Serialized subject data or an error message.
        """
        try:
            logger.info(f"Fetching enrolled subjects for user: {request.user.username}")
            student = Student.objects.get(user=request.user)
            subjects = student.enrolled_subjects.all()
            serializer = SubjectSerializer(subjects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching enrolled subjects: {e}")
            return Response({'error': 'An unexpected error occurred.', 'details': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
