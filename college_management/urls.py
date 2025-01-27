from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core_api.views.auth_views import LoginView, LogoutView
from core_api.views.faculty_views import FacultyViewSet
from core_api.views.student_views import StudentViewSet
from core_api.views.subject_views import SubjectViewSet
from django.conf import settings
from django.conf.urls.static import static

# Initialize the router
router = DefaultRouter()

# Register viewsets with the router
router.register(r'faculty', FacultyViewSet, basename='faculty')
router.register(r'students', StudentViewSet, basename='students')
router.register(r'subjects', SubjectViewSet, basename='subjects')

# Define URL patterns
urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Authentication endpoints
    path('api/login/', LoginView.as_view(), name='login'),  # Login endpoint
    path('api/logout/', LogoutView.as_view(), name='logout'),  # Logout endpoint

    # Router-based endpoints for CRUD operations
    path('api/', include(router.urls)),

    # Faculty-specific custom routes
    path(
        'api/faculty/<int:pk>/assign-student/',
        FacultyViewSet.as_view({'post': 'assign_student'}),
        name='faculty-assign-student',
    ),
    path(
        'api/faculty/<int:pk>/unassign-student/',
        FacultyViewSet.as_view({'post': 'unassign_student'}),
        name='faculty-unassign-student',
    ),
    path(
        'api/faculty/<int:pk>/students/',
        FacultyViewSet.as_view({'get': 'get_students'}),
        name='faculty-students',
    ),
    path('api/faculty/<int:pk>/unassigned-students/', 
        FacultyViewSet.as_view({'get': 'unassigned_students'}),
        name='unassigned-students'),


    # Student-specific custom routes
    path(
        'api/students/<int:pk>/enrolled-subjects/',
        StudentViewSet.as_view({'get': 'get_enrolled_subjects'}),
        name='student-enrolled-subjects',
    ),
    path('api/students/me/', 
         StudentViewSet.as_view({'get': 'get_logged_in_student'}), 
         name='student-detail',
    ),
    path(
        'api/students/me/enrolled-subjects/',
        StudentViewSet.as_view({'get': 'get_logged_in_student_subjects'}),
        name= 'subject-details',
    ),
    

    # Subject-specific custom routes
    path(
        'api/subjects/<int:pk>/enrolled-students/',
        SubjectViewSet.as_view({'get': 'get_enrolled_students'}),
        name='subject-enrolled-students',
    ),
    path(
        'api/subjects/<int:pk>/teaching-faculty/',
        SubjectViewSet.as_view({'get': 'get_teaching_faculty'}),
        name='subject-teaching-faculty',
    ),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
