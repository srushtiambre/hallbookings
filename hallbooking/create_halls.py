import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hallbooking.settings')
django.setup()

from bookings.models import Hall

halls_data = [
    {
        'name': 'Saibaba Hall',
        'capacity': 500,
        'location': 'Main Building, Ground Floor',
        'description': 'Large auditorium suitable for major events and gatherings. Amenities removed.',
        'amenities': '',
    },
    {
        'name': 'New Seminar Hall',
        'capacity': 200,
        'location': 'Science Block, 2nd Floor',
        'description': 'Modern seminar hall equipped for academic presentations. Amenities removed.',
        'amenities': '',
    },
    {
        'name': 'Bandulal Bafna Hall',
        'capacity': 300,
        'location': 'Commerce Wing',
        'description': 'Spacious hall for conferences and cultural programs. Amenities removed.',
        'amenities': '',
    }
]

for data in halls_data:
    hall, created = Hall.objects.update_or_create(
        name=data['name'],
        defaults={
            'capacity': data['capacity'],
            'location': data['location'],
            'description': data['description'],
            'amenities': data['amenities']
        }
    )
    
    if created:
        print(f"Created hall: {hall.name}")
    else:
        print(f"Updated hall: {hall.name}")

# Also verify no other halls have amenities if needed, or just rely on these 3.
# For completeness, let's clear amenities from any other halls if they existed, 
# although request was likely just for these.
# Hall.objects.exclude(name__in=[h['name'] for h in halls_data]).update(amenities='')

print("\nHall amenities removed and updated.")
