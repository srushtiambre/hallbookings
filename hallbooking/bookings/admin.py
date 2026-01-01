from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from .models import Hall, Booking


class HallBookingAdminSite(AdminSite):
    """Custom admin site for Hall Booking System"""
    site_header = "Hall Booking Administration"
    site_title = "Hall Booking Admin"
    index_title = "Welcome to Hall Booking Administration"
    
    def each_context(self, request):
        context = super().each_context(request)
        context['site_header'] = self.site_header
        context['site_title'] = self.site_title
        return context


# Create custom admin site instance
admin_site = HallBookingAdminSite(name='hallbooking_admin')


@admin.register(Hall, site=admin_site)
class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'location', 'available', 'created_at']
    list_filter = ['capacity', 'available', 'created_at']
    search_fields = ['name', 'location', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'capacity', 'location')
        }),
        ('Details', {
            'fields': ('description', 'amenities', 'image')
        }),
        ('Status', {
            'fields': ('available', 'created_at')
        }),
    )
    
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return list_display
    
    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }


@admin.register(Booking, site=admin_site)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'hall_name', 'user_name', 'booking_date', 'time_slot', 'status_badge', 'purpose']
    list_filter = ['status', 'booking_date', 'hall', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'hall__name', 'purpose']
    date_hierarchy = 'booking_date'
    ordering = ['-booking_date', '-created_at']
    
    fieldsets = (
        ('Booking Details', {
            'fields': ('hall', 'user', 'booking_date', 'start_time', 'end_time')
        }),
        ('Event Information', {
            'fields': ('purpose', 'expected_attendees')
        }),
        ('Approval Status', {
            'fields': ('status', 'approved_by', 'rejection_reason'),
            'description': 'Manage the approval workflow for this booking.'
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
    actions = ['approve_bookings', 'reject_bookings']
    
    def booking_id(self, obj):
        return f"#{obj.id}"
    booking_id.short_description = "ID"
    
    def hall_name(self, obj):
        return obj.hall.name
    hall_name.short_description = "Hall"
    
    def user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_name.short_description = "Requested By"
    
    def time_slot(self, obj):
        return f"{obj.start_time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"
    time_slot.short_description = "Time"
    
    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'approved': '#10b981',
            'rejected': '#ef4444',
            'cancelled': '#6b7280',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"
    
    def approve_bookings(self, request, queryset):
        updated = 0
        for booking in queryset.filter(status='pending'):
            booking.status = 'approved'
            booking.approved_by = request.user
            booking.rejection_reason = ''
            booking.save()
            updated += 1
        self.message_user(request, f'{updated} booking(s) approved successfully.')
    approve_bookings.short_description = "✓ Approve selected bookings"
    
    def reject_bookings(self, request, queryset):
        updated = 0
        for booking in queryset.filter(status='pending'):
            booking.status = 'rejected'
            booking.approved_by = request.user
            booking.save()
            updated += 1
        self.message_user(request, f'{updated} booking(s) rejected successfully.')
    reject_bookings.short_description = "✗ Reject selected bookings"
    
    def save_model(self, request, obj, form, change):
        if obj.status == 'approved' and not obj.approved_by:
            obj.approved_by = request.user
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }
