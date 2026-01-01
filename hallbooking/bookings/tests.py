# Hall Booking System Tests

from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Hall, Booking


class HallModelTest(TestCase):
    def setUp(self):
        self.hall = Hall.objects.create(
            name='Test Hall',
            capacity=100,
            location='Test Location',
            description='Test Description',
            amenities='WiFi, AC'
        )

    def test_hall_creation(self):
        self.assertEqual(self.hall.name, 'Test Hall')
        self.assertEqual(self.hall.capacity, 100)

    def test_hall_string_representation(self):
        self.assertEqual(str(self.hall), 'Test Hall (100 capacity)')


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.hall = Hall.objects.create(
            name='Test Hall',
            capacity=100,
            location='Test Location',
            description='Test Description'
        )

    def test_booking_creation(self):
        tomorrow = datetime.now().date() + timedelta(days=1)
        booking = Booking.objects.create(
            hall=self.hall,
            user=self.user,
            booking_date=tomorrow,
            start_time='10:00',
            end_time='12:00',
            purpose='Test Event',
            expected_attendees=50,
            status='pending'
        )
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.expected_attendees, 50)
