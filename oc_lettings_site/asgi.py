"""ASGI entry point of the project.

Exposes the ``application`` callable that asynchronous servers use to serve the site.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')

application = get_asgi_application()
