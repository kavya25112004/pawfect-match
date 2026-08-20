from django.db import models

# Create your models here.

from django.conf import settings

class DoctorBooking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vet_bookings')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_appointments')
    pet_name = models.CharField(max_length=100)
    pet_breed = models.CharField(max_length=100)
    issue_description = models.TextField()
    booking_date = models.DateField()
    booking_time = models.TimeField()
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.pet_name} with Dr. {self.doctor.username} ({self.status})"