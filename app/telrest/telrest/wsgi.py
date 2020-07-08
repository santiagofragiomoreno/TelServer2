"""
WSGI config for telrest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

paths = [
    '/var/www/TelServer/app/telrest/telrest/static',
]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telrest.settings')

application = get_wsgi_application()
