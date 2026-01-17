import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmedia_backend.settings')
django.setup()

from users.models import User

# Create principal user
try:
    # Delete existing principal if exists
    User.objects.filter(email='principal@gmail.com').delete()
    
    principal_user = User(
        first_name='Principal',
        last_name='User',
        email='principal@gmail.com',
        register_number='PRIN001',
        phone='0000000001',
        role='Principal',
        password='principal@123'  # Will be hashed by save() method
    )
    principal_user.save()
    
    print("✅ Principal user created successfully!")
    print(f"Email: principal@gmail.com")
    print(f"Password: principal@123")
    print(f"Register Number: PRIN001")
    print(f"Role: Principal")
    print("\n💡 Login with:")
    print("   Email: principal@gmail.com")
    print("   Password: principal@123")
except Exception as e:
    print(f"❌ Error creating principal user: {e}")
