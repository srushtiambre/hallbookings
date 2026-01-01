from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hall/<int:hall_id>/', views.hall_detail, name='hall_detail'),
    path('hall/<int:hall_id>/book/', views.book_hall, name='book_hall'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('api/check-availability/', views.check_availability, name='check_availability'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='bookings/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.index, name='register'),  # Placeholder
    path('pending-bookings/', views.pending_bookings, name='pending_bookings'),
    path('booking/<int:booking_id>/approve/', views.approve_booking, name='approve_booking'),
    path('booking/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
]
