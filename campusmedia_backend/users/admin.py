from django.contrib import admin
from .models import User, Class, ClassEnrollment, Attendance, Grade, Announcement

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('register_number', 'first_name', 'last_name', 'email', 'role', 'phone', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'register_number', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Campus Information', {
            'fields': ('register_number', 'role')
        }),
        ('Security', {
            'fields': ('password',),
            'description': 'Password is automatically hashed when saved.'
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'subject', 'teacher', 'student_count', 'schedule', 'is_active', 'created_at')
    list_filter = ('is_active', 'teacher', 'created_at')
    search_fields = ('class_name', 'subject', 'teacher__first_name', 'teacher__last_name')
    ordering = ('class_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ClassEnrollment)
class ClassEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_enrolled', 'enrolled_at')
    list_filter = ('class_enrolled', 'enrolled_at')
    search_fields = ('student__first_name', 'student__last_name', 'class_enrolled__class_name')
    ordering = ('-enrolled_at',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_attended', 'date', 'status', 'marked_by', 'created_at')
    list_filter = ('status', 'date', 'class_attended', 'marked_by')
    search_fields = ('student__first_name', 'student__last_name', 'class_attended__class_name')
    ordering = ('-date', 'class_attended')
    readonly_fields = ('created_at',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_graded', 'assignment_name', 'score', 'grade_letter', 'graded_by', 'created_at')
    list_filter = ('grade_letter', 'class_graded', 'graded_by', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'class_graded__class_name', 'assignment_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'grade_letter')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'target_role', 'is_active', 'created_at')
    list_filter = ('is_active', 'target_role', 'created_at', 'created_by')
    search_fields = ('title', 'content', 'created_by__first_name', 'created_by__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
