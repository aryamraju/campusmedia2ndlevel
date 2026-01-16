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
    
    # Additional fields
    is_active = models.BooleanField(default=True)
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
