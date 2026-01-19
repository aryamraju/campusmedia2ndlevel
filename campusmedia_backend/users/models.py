from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    """
    User model for CampusMedia platform
    Based on the registration form fields
    """
    ROLE_CHOICES = [
        ('User', 'User'),
        ('Student', 'Student'),
        ('Staff', 'Staff'),
        ('Principal', 'Principal'),
        ('Admin', 'Admin'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    register_number = models.CharField(max_length=50, unique=True, help_text="Campus ID or Register Number")
    phone = models.CharField(max_length=10)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='User')
    password = models.CharField(max_length=255)
    
    # Student-specific fields
    student_class = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 10th Grade, BSc Year 1")
    stream = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Science, Commerce, Arts")
    year = models.CharField(max_length=20, blank=True, null=True, help_text="e.g., 2024, Freshman")
    department = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Computer Science")
    
    # Staff-specific fields
    qualification = models.CharField(max_length=200, blank=True, null=True, help_text="e.g., M.Sc Physics, B.Ed")
    subject_expertise = models.CharField(max_length=200, blank=True, null=True, help_text="e.g., Mathematics, Physics")
    assigned_classes = models.TextField(blank=True, null=True, help_text="Classes assigned to teach")
    experience_years = models.IntegerField(blank=True, null=True, help_text="Years of teaching experience")
    
    # Additional fields
    is_active = models.BooleanField(default=True)
    profile_completed = models.BooleanField(default=False, help_text="Has user completed their profile details")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.register_number})"
    
    def save(self, *args, **kwargs):
        # Hash password before saving if it's not already hashed
        if self.pk is None or not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def check_password(self, raw_password):
        """
        Verify a raw password against the hashed password
        """
        return check_password(raw_password, self.password)
    
    def get_full_name(self):
        """
        Returns the user's full name
        """
        return f"{self.first_name} {self.last_name}"


class Class(models.Model):
    """
    Class model for managing classes taught by staff
    """
    class_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    schedule = models.CharField(max_length=255, help_text="e.g., Mon, Wed, Fri • 9:00 AM - 10:30 AM")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes_taught', limit_choices_to={'role__in': ['Staff', 'Principal']})
    student_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'classes'
        ordering = ['class_name']
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
    
    def __str__(self):
        return f"{self.class_name} - {self.subject}"


class ClassEnrollment(models.Model):
    """
    Enrollment of students in classes
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_classes', limit_choices_to={'role': 'Student'})
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'class_enrollments'
        unique_together = ['student', 'class_enrolled']
        verbose_name = 'Class Enrollment'
        verbose_name_plural = 'Class Enrollments'
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.class_enrolled.class_name}"


class Attendance(models.Model):
    """
    Attendance records for students in classes
    """
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records', limit_choices_to={'role': 'Student'})
    class_attended = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Present')
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_attendance', limit_choices_to={'role__in': ['Staff', 'Principal']})
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'attendance'
        ordering = ['-date', 'class_attended']
        unique_together = ['student', 'class_attended', 'date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.class_attended.class_name} - {self.date} - {self.status}"


class Grade(models.Model):
    """
    Grade records for students in classes
    """
    GRADE_CHOICES = [
        ('A', 'A (90-100)'),
        ('B', 'B (80-89)'),
        ('C', 'C (70-79)'),
        ('D', 'D (60-69)'),
        ('F', 'F (Below 60)'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades', limit_choices_to={'role': 'Student'})
    class_graded = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='grades')
    assignment_name = models.CharField(max_length=255)
    score = models.IntegerField(help_text="Score out of 100")
    grade_letter = models.CharField(max_length=1, choices=GRADE_CHOICES)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='grades_given', limit_choices_to={'role__in': ['Staff', 'Principal']})
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grades'
        ordering = ['-created_at']
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.class_graded.class_name} - {self.assignment_name} - {self.grade_letter}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate grade letter based on score
        if self.score >= 90:
            self.grade_letter = 'A'
        elif self.score >= 80:
            self.grade_letter = 'B'
        elif self.score >= 70:
            self.grade_letter = 'C'
        elif self.score >= 60:
            self.grade_letter = 'D'
        else:
            self.grade_letter = 'F'
        super().save(*args, **kwargs)


class Announcement(models.Model):
    """
    Announcements created by staff/principal
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements', limit_choices_to={'role__in': ['Staff', 'Principal', 'Admin']})
    target_role = models.CharField(max_length=20, blank=True, null=True, help_text="Leave empty for all users")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
    
    def __str__(self):
        return f"{self.title} by {self.created_by.get_full_name()}"
