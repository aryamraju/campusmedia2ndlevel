import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmedia_backend.settings')
django.setup()

from users.models import User

user = User.objects.filter(email='ammu@gmail.com').first()
if user:
    print(f'✅ User Found!')
    print(f'Name: {user.first_name} {user.last_name}')
    print(f'Email: {user.email}')
    print(f'Role: {user.role}')
    print(f'User ID: {user.id}')
    print(f'Profile Completed: {user.profile_completed}')
else:
    print('❌ User not found with email ammu@gmail.com')
