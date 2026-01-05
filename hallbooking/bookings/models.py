from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


class Hall(models.Model):
    """Model for college halls available for booking"""
    CAPACITY_CHOICES = [
        (100, '100 people'),
        (200, '200 people'),
        (300, '300 people'),
        (500, '500 people'),
    ]
    
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(choices=CAPACITY_CHOICES)
    location = models.CharField(max_length=200)
    description = models.TextField()
    amenities = models.TextField(help_text="List amenities separated by comma")
    image = models.CharField(max_length=200, default='hall-placeholder.jpg')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.capacity} capacity)"
    
    @property
    def amenities_list(self):
        """Return amenities as a list of trimmed strings."""
        if not self.amenities:
            return []
        return [a.strip() for a in self.amenities.split(',') if a.strip()]
    
    def is_available_on_date(self, date):
        """Check if hall is available on a specific date"""
        bookings = self.booking_set.filter(
            booking_date=date,
            status__in=['pending', 'approved']
        )
        return not bookings.exists()


class Booking(models.Model):
    """Model for hall bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    purpose = models.CharField(max_length=200)
    expected_attendees = models.IntegerField()
    faculty = models.CharField(max_length=50, choices=[('Arts', 'Arts'), ('Commerce', 'Commerce'), ('Science', 'Science')], default='Science')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='approved_bookings'
    )
    rejection_reason = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-booking_date']
        unique_together = ('hall', 'booking_date', 'start_time')
    
    def __str__(self):
        return f"{self.hall.name} - {self.booking_date} ({self.status})"
    
    def clean(self):
        """Validate booking data"""
        if self.booking_date < datetime.now().date():
            raise ValidationError("Booking date cannot be in the past")
        
        if self.expected_attendees > self.hall.capacity:
            raise ValidationError(f"Expected attendees exceed hall capacity of {self.hall.capacity}")
        
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")
        
        # Check for conflicting bookings
        conflicting = Booking.objects.filter(
            hall=self.hall,
            booking_date=self.booking_date,
            status__in=['pending', 'approved']
        ).exclude(id=self.id)
        
        for booking in conflicting:
            if not (self.end_time <= booking.start_time or self.start_time >= booking.end_time):
                raise ValidationError("Time slot conflicts with existing booking")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
