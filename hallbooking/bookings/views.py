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


from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('index')
    else:
        form = UserCreationForm()
    
    return render(request, 'bookings/register.html', {'form': form})

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
            expected_attendees_val = request.POST.get('expected_attendees')
            if not expected_attendees_val:
                raise ValueError("Expected attendees is required")
            expected_attendees = int(expected_attendees_val)
            faculty = request.POST.get('faculty')
            
            booking = Booking(
                hall=hall,
                user=request.user,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time,
                purpose=purpose,
                expected_attendees=expected_attendees,
                faculty=faculty,
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
    if request.user.is_staff:
        return redirect('admin_dashboard')
        
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


@staff_member_required
def admin_dashboard(request):
    """Admin dashboard to manage bookings and halls"""
    context = {
        'pending_count': Booking.objects.filter(status='pending').count(),
        'total_halls': Hall.objects.count(),
    }
    return render(request, 'bookings/admin_dashboard.html', context)

from .forms import HallForm

@staff_member_required
def manage_halls(request):
    """List and manage halls"""
    halls = Hall.objects.all()
    return render(request, 'bookings/manage_halls.html', {'halls': halls})

@staff_member_required
def add_hall(request):
    """Add a new hall"""
    if request.method == 'POST':
        form = HallForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New hall added successfully!')
            return redirect('manage_halls')
    else:
        form = HallForm()
    return render(request, 'bookings/hall_form.html', {'form': form})

@staff_member_required
def edit_hall(request, hall_id):
    """Edit an existing hall"""
    hall = get_object_or_404(Hall, id=hall_id)
    if request.method == 'POST':
        form = HallForm(request.POST, instance=hall)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hall updated successfully!')
            return redirect('manage_halls')
    else:
        form = HallForm(instance=hall)
    return render(request, 'bookings/hall_form.html', {'form': form})

@staff_member_required
def delete_hall(request, hall_id):
    """Delete a hall"""
    hall = get_object_or_404(Hall, id=hall_id)
    if request.method == 'POST':
        hall.delete()
        messages.success(request, 'Hall deleted successfully!')
        return redirect('manage_halls')
    return render(request, 'bookings/hall_confirm_delete.html', {'hall': hall})


from django.db.models import Count

@staff_member_required
def admin_reports(request):
    """View booking reports"""
    # Summary stats
    total_bookings = Booking.objects.count()
    status_counts = Booking.objects.values('status').annotate(count=Count('id'))
    
    # Hall popularity
    hall_stats = Booking.objects.values('hall__name').annotate(count=Count('id')).order_by('-count')
    
    # Recent activity
    recent_bookings = Booking.objects.select_related('user', 'hall').order_by('-created_at')[:10]
    
    context = {
        'total_bookings': total_bookings,
        'status_counts': status_counts,
        'hall_stats': hall_stats,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'bookings/admin_reports.html', context)
