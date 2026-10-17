"""Register the lettings models in the Django admin interface."""

from django.contrib import admin

from .models import Letting
from .models import Address

admin.site.register(Letting)
admin.site.register(Address)
