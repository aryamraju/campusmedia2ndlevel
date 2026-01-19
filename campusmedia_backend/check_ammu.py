import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmedia_backend.settings')
django.setup()

from users.models import User

u = User.objects.filter(email='ammu@gmail.com').first()
if u:
    print('Name:', u.first_name, u.last_name)
    print('Email:', u.email)
    print('Phone:', u.phone)
    print('Register Number:', u.register_number)
