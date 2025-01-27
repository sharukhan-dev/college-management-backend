from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from core_api.models.faculty import Faculty
from core_api.models.student import Student
from core_api.models.subject import Subject
from core_api.serializers.faculty_serializer import FacultySerializer
from core_api.serializers.student_serializer import StudentSerializer


class FacultyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for faculty operations.
    Allows faculty to assign/unassign students to subjects and fetch assigned students.
    """
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access these endpoints

    def get_queryset(self):
        """
        Return only the faculty details for the logged-in user.
        """
        user = self.request.user
        if user.user_type == 1:  # If the user is a faculty
            return Faculty.objects.filter(user=user)
        elif user.is_superuser:  # If the user is an admin
            return Faculty.objects.all()
        return Faculty.objects.none()  # Restrict students to their own details

    
    def get_subject_for_faculty(self, faculty):
        """
        Utility method to fetch the subject taught by a specific faculty.
        """
        try:
            return Subject.objects.get(faculty=faculty)
        except Subject.DoesNotExist:
            return None


    def assign_student(self, request, pk=None):
        try:
            faculty = self.get_object()
            subject = self.get_subject_for_faculty(faculty)
            if not subject:
                return Response({'error': 'Faculty has no assigned subject.'}, status=400)

            student_id = request.data.get('student_id')
            if not student_id:
                return Response({'error': 'Student ID is required.'}, status=400)

            student = Student.objects.get(pk=student_id)

            if subject not in student.enrolled_subjects.all():
                student.enrolled_subjects.add(subject)
                student.save()

            return Response({'message': f'Subject "{subject.name}" assigned to student {student.user.username}.'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)



    def unassign_student(self, request, pk=None):
        """
        Unassign a student from a faculty's subject.
        """
        try:
            faculty = self.get_object()
            subject = self.get_subject_for_faculty(faculty)

            if not subject:
                return Response(
                    {'error': 'Faculty is not assigned to any subject.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            student_id = request.data.get('student_id')
            if not student_id:
                return Response({'error': 'Student ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            student = Student.objects.get(pk=student_id)
            student.enrolled_subjects.remove(subject)
            return Response({'message': f'Student {student.first_name} unassigned from {subject.name}.'}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Failed to unassign student.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_students(self, request, pk=None):
        """
        Fetch all students assigned to a faculty's subject.
        """
        try:
            faculty = self.get_object()
            subject = self.get_subject_for_faculty(faculty)

            if not subject:
                return Response({'error': 'Faculty has no assigned subject.'}, status=400)

            students = Student.objects.filter(enrolled_subjects=subject)
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=200)

        except Faculty.DoesNotExist:
            return Response({'error': 'Faculty not found.'}, status=404)
        except Exception as e:
            # print(f"Error fetching students: {str(e)}")
            return Response({'error': str(e)}, status=500)



    def unassigned_students(self, request, pk=None):
        """
        Fetch students who are not assigned to any subject of this faculty.
        """
        try:
            faculty = self.get_object()
            subject = self.get_subject_for_faculty(faculty)

            # Fetch students not enrolled in this specific subject
            students = Student.objects.exclude(enrolled_subjects=subject)

            # # Debugging: Log the list of unassigned students
            # print(f"Unassigned Students for Faculty: {faculty.user.username}")
            # for student in students:
            #     print(f"- Student: {student.user.username}, Enrolled Subjects: {[sub.name for sub in student.enrolled_subjects.all()]}")
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # print("Error fetching unassigned students:", str(e))
            return Response({'error': 'Failed to fetch unassigned students.', 'details': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

