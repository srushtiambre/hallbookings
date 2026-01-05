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
    path('admin-login/', auth_views.LoginView.as_view(template_name='bookings/admin_login.html', next_page='admin_dashboard'), name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # Admin Panel URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-halls/', views.manage_halls, name='manage_halls'),
    path('add-hall/', views.add_hall, name='add_hall'),
    path('edit-hall/<int:hall_id>/', views.edit_hall, name='edit_hall'),
    path('delete-hall/<int:hall_id>/', views.delete_hall, name='delete_hall'),
    path('admin-reports/', views.admin_reports, name='admin_reports'),

    path('pending-bookings/', views.pending_bookings, name='pending_bookings'),
    path('booking/<int:booking_id>/approve/', views.approve_booking, name='approve_booking'),
    path('booking/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
]
