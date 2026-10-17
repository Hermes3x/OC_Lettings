"""Configuration of the lettings application."""

from django.apps import AppConfig


class LettingsConfig(AppConfig):
    """Register the lettings application with Django.

    Attributes:
        name (str): the Python path of the application, used in INSTALLED_APPS.
    """
    name = 'lettings'
