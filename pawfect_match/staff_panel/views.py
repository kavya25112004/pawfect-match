from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DoctorBooking
from accounts.models import DoctorProfile

# 1. Doctor Dashboard View (To view profile and incoming appointment requests)
@login_required
def doctor_dashboard_view(request):
    # Logged-in doctor's profile details
    profile = DoctorProfile.objects.filter(user=request.user).first()
    
    # Bookings assigned to this specific doctor
    bookings = DoctorBooking.objects.filter(doctor=request.user).order_by('-created_at')

    context = {
        'profile': profile,
        'bookings': bookings,
        'appointments':bookings
    }
    return render(request, 'doctor_dashboard.html', context)

# 2. Update Booking Status (Accept / Reject / Complete)
@login_required
def update_booking_status_view(request, booking_id, status):
    booking = get_object_or_404(DoctorBooking, id=booking_id, doctor=request.user)
    if status.lower() in ['accepted', 'rejected', 'completed','confirmed','cancelled']:
        booking.status = status.capitalize()
        booking.save()
        messages.success(request, f'Appointment marked as {status.capitalize()}.')
    return redirect('staff_panel:dashboard')
