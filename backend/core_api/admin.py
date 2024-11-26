from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Faculty, Student, Subject

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model.
    Includes user_type management and filters for ease of access.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Custom fields', {'fields': ('user_type',)}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type'),
        }),
    )


admin.site.register(User, CustomUserAdmin)

# Faculty Admin
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'profile_pic', 'created_at', 'updated_at')  # Include timestamps
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__is_active', 'created_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            linked_users = Faculty.objects.values_list('user', flat=True)
            kwargs["queryset"] = User.objects.filter(is_superuser=False).exclude(id__in=linked_users)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"

# Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'contact_number', 'blood_group', 'created_at', 'updated_at')  # Include timestamps
    search_fields = ('user__username', 'first_name', 'last_name', 'contact_number')
    list_filter = ('gender', 'blood_group', 'created_at')

# Subject Admin
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_faculty', 'created_at', 'updated_at')  # Include timestamps
    search_fields = ('name', 'faculty__user__username', 'faculty__user__email')
    list_filter = ('faculty__user__is_active', 'created_at')

    def get_faculty(self, obj):
        return obj.faculty.user.username
    get_faculty.short_description = "Faculty"
