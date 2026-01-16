import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmedia_backend.settings')
django.setup()

from users.models import User

print("=" * 60)
print("Admin User Details")
print("=" * 60)

try:
    admin = User.objects.get(email='admin@gmail.com')
    print(f"\n✅ Admin user found in database:")
    print(f"   ID: {admin.id}")
    print(f"   Name: {admin.first_name}")
    print(f"   Email: {admin.email}")
    print(f"   Role: {admin.role}")
    print(f"   Register Number: {admin.register_number}")
    print(f"   Phone: {admin.phone}")
    print(f"   Active: {admin.is_active}")
    print(f"   Created: {admin.created_at}")
    
    # Test password
    if admin.check_password('admin@123'):
        print(f"\n✅ Password 'admin@123' verified successfully!")
    else:
        print(f"\n❌ Password verification failed!")
        
except User.DoesNotExist:
    print("\n❌ Admin user not found!")
    
print("\n" + "=" * 60)
print("All Users in Database:")
print("=" * 60)
all_users = User.objects.all()
print(f"Total users: {all_users.count()}")
for user in all_users:
    print(f"  - {user.email} ({user.role})")
