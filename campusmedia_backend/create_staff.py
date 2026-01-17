import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmedia_backend.settings')
django.setup()

from users.models import User

# Create staff user
staff = User(
    email='staff@gmail.com',
    password='staff@123',  # Will be hashed in save()
    role='Staff',
    first_name='Test',
    last_name='Staff',
    phone='9876543210',
    register_number='STAFF001'
)
staff.save()
print(f"Staff user created: {staff.email}")
