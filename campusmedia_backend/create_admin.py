import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmedia_backend.settings')
django.setup()

from users.models import User

# Create admin user
try:
    admin_user = User.objects.create(
        first_name='Admin',
        last_name='',
        email='admin@gmail.com',
        register_number='ADMIN001',
        phone='0000000000',
        role='Admin',
        password='admin@123'  # Will be automatically hashed by the model
    )
    print("✅ Admin user created successfully!")
    print(f"Email: {admin_user.email}")
    print(f"Role: {admin_user.role}")
    print(f"Register Number: {admin_user.register_number}")
except Exception as e:
    print(f"❌ Error creating admin user: {e}")
