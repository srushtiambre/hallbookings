import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hallbooking.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

users = [
    {
        'username': 'student1',
        'email': 'student1@college.edu',
        'password': 'studentpass',
        'is_superuser': False,
        'is_staff': False,
    },
    {
        'username': 'admin',
        'email': 'admin@college.edu',
        'password': 'admin',
        'is_superuser': True,
        'is_staff': True,
    }
]

for u in users:
    if not User.objects.filter(username=u['username']).exists():
        user = User.objects.create_user(username=u['username'], email=u['email'], password=u['password'])
        user.is_staff = u['is_staff']
        user.is_superuser = u['is_superuser']
        user.save()
        print(f"Created user: {u['username']} (superuser={u['is_superuser']})")
    else:
        print(f"User already exists: {u['username']}")

print('\nTest users are ready:')
print(' - student1 / studentpass  (regular user)')
print(' - admin / admin  (superuser)')
