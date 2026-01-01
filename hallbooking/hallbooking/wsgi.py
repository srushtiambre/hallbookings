"""
WSGI config for hallbooking project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hallbooking.settings')

application = get_wsgi_application()
