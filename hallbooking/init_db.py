import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hallbooking.settings')
django.setup()

from django.contrib.auth.models import User
from bookings.models import Hall

# Create default halls
halls_data = [
    {
        'name': 'Auditorium A',
        'capacity': 500,
        'location': 'Main Building, 1st Floor',
        'description': 'Large auditorium with state-of-the-art audio-visual equipment, perfect for conferences and major events.',
        'amenities': 'Projector, Sound System, Stage, WiFi, AC, Parking',
    },
    {
        'name': 'Conference Hall B',
        'capacity': 300,
        'location': 'Academic Block, 3rd Floor',
        'description': 'Modern conference hall with flexible seating arrangement, ideal for seminars and corporate events.',
        'amenities': 'Video Conferencing, Board Room Setup, WiFi, AC, Refreshment Counter',
    },
    {
        'name': 'Seminar Room C',
        'capacity': 100,
        'location': 'Library Building, 2nd Floor',
        'description': 'Intimate seminar room perfect for workshops, training sessions, and small meetings.',
        'amenities': 'Whiteboard, Projector, WiFi, AC, Discussion Tables',
    },
    {
        'name': 'Banquet Hall D',
        'capacity': 200,
        'location': 'Student Center',
        'description': 'Elegant banquet hall with full catering facilities, perfect for celebrations and formal dinners.',
        'amenities': 'Catering Kitchen, Elegant Decor, Sound System, Dance Floor, AC, Ample Parking',
    },
]

for hall_data in halls_data:
    hall, created = Hall.objects.get_or_create(
        name=hall_data['name'],
        defaults=hall_data
    )
    if created:
        print(f"✓ Created hall: {hall.name}")
    else:
        print(f"ℹ Hall already exists: {hall.name}")

print("\n✓ Database initialization complete!")
print("You can now use the admin panel at: http://localhost:8000/admin/")
print("Default superuser: admin (password: admin)")
