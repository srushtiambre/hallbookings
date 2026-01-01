"""
URL configuration for hallbooking project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from bookings.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('bookings.urls')),
    # Keep old Django default post-login path working
    path('accounts/profile/', RedirectView.as_view(pattern_name='my_bookings', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)