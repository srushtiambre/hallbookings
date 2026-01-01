from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
from .models import Hall, Booking
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt


def index(request):
    """Home page with hall listing"""
    halls = Hall.objects.filter(available=True)
    context = {
        'halls': halls,
        'total_halls': halls.count(),
    }
    return render(request, 'bookings/index.html', context)


def hall_detail(request, hall_id):
    """Display hall details and bookings"""
    hall = get_object_or_404(Hall, id=hall_id)
    bookings = Booking.objects.filter(
        hall=hall,
        status__in=['approved', 'pending']
    ).order_by('booking_date', 'start_time')
    
    context = {
        'hall': hall,
        'bookings': bookings,
        'amenities': hall.amenities_list,
    }
    return render(request, 'bookings/hall_detail.html', context)


@login_required(login_url='login')
def book_hall(request, hall_id):
    """Create a new booking"""
    hall = get_object_or_404(Hall, id=hall_id)
    
    if request.method == 'POST':
        try:
            booking_date = request.POST.get('booking_date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            purpose = request.POST.get('purpose')
            expected_attendees = int(request.POST.get('expected_attendees'))
            
            booking = Booking(
                hall=hall,
                user=request.user,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time,
                purpose=purpose,
                expected_attendees=expected_attendees,
                status='pending'
            )
            booking.full_clean()
            booking.save()
            
            messages.success(request, f'Booking request submitted for {hall.name}!')
            return redirect('booking_confirmation', booking_id=booking.id)
        
        except Exception as e:
            messages.error(request, f'Error creating booking: {str(e)}')
    
    context = {'hall': hall}
    return render(request, 'bookings/book_hall.html', context)


@login_required(login_url='login')
def booking_confirmation(request, booking_id):
    """Show booking confirmation"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    context = {'booking': booking}
    return render(request, 'bookings/booking_confirmation.html', context)


@login_required(login_url='login')
def my_bookings(request):
    """Display user's bookings"""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
        'pending_count': bookings.filter(status='pending').count(),
        'approved_count': bookings.filter(status='approved').count(),
    }
    return render(request, 'bookings/my_bookings.html', context)


@login_required(login_url='login')
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status in ['pending', 'approved']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully!')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    
    return redirect('my_bookings')


@require_http_methods(["GET"])
def check_availability(request):
    """AJAX endpoint to check hall availability"""
    hall_id = request.GET.get('hall_id')
    booking_date = request.GET.get('date')
    
    if not hall_id or not booking_date:
        return JsonResponse({'available': False})
    
    try:
        hall = Hall.objects.get(id=hall_id)
        is_available = hall.is_available_on_date(booking_date)
        return JsonResponse({'available': is_available})
    except Hall.DoesNotExist:
        return JsonResponse({'available': False})


@require_POST
def logout_view(request):
    """Log out user via POST and redirect to index."""
    logout(request)
    return redirect('index')


@staff_member_required
def pending_bookings(request):
    """List all pending bookings for staff to review."""
    bookings = Booking.objects.filter(status='pending').order_by('booking_date', 'start_time')
    return render(request, 'bookings/pending_bookings.html', {'bookings': bookings})


@staff_member_required
@require_POST
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'approved'
    booking.approved_by = request.user
    booking.rejection_reason = ''
    booking.save()
    messages.success(request, f'Booking #{booking.id} approved.')
    return redirect('pending_bookings')


@staff_member_required
@require_POST
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    reason = request.POST.get('rejection_reason', '')
    booking.status = 'rejected'
    booking.rejection_reason = reason
    booking.approved_by = request.user
    booking.save()
    messages.success(request, f'Booking #{booking.id} rejected.')
    return redirect('pending_bookings')
