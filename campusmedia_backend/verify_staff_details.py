import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmedia_backend.settings')
django.setup()

from users.models import User

# Get all staff users and display their details
print("Staff Users in Database:")
print("=" * 80)

staff_users = User.objects.filter(role='Staff')

for staff in staff_users:
    print(f"\nStaff ID: {staff.id}")
    print(f"Name: {staff.first_name} {staff.last_name}")
    print(f"Email: {staff.email}")
    print(f"Register Number: {staff.register_number}")
    print(f"Qualification: {staff.qualification}")
    print(f"Subject Expertise: {staff.subject_expertise}")
    print(f"Assigned Classes: {staff.assigned_classes}")
    print(f"Experience Years: {staff.experience_years}")
    print("-" * 80)

print(f"\nTotal Staff Users: {staff_users.count()}")
