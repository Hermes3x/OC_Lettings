"""Configuration of the profiles application."""

from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """Register the profiles application with Django.

    Attributes:
        name (str): the Python path of the application, used in INSTALLED_APPS.
    """
    name = 'profiles'
