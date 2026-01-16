from django.contrib import admin
from .models import User

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
