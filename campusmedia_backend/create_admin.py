import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmedia_backend.settings')
django.setup()

from users.models import User

# Create admin user with specific credentials
try:
    # Delete existing admin if exists
    User.objects.filter(email='admin@gmail.com').delete()
    
    admin_user = User(
        first_name='Admin',
        last_name='User',
        email='admin@gmail.com',
        register_number='ADMIN2026',  # Using secret key as register number
        phone='0000000000',
        role='Admin',
        password='admin@123'  # Will be hashed by save() method
    )
    admin_user.save()
    
    print("✅ Admin user created successfully!")
    print(f"Email: admin@gmail.com")
    print(f"Password: admin@123")
    print(f"Secret Key/Register Number: ADMIN2026")
    print(f"Role: Admin")
    print("\n💡 Login with:")
    print("   Email: admin@gmail.com")
    print("   Password: admin@123")
    print("   Secret Key: ADMIN2026")
except Exception as e:
    print(f"❌ Error creating admin user: {e}")
