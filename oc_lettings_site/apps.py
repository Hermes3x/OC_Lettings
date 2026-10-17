"""Configuration of the oc_lettings_site application."""

from django.apps import AppConfig


class OCLettingsSiteConfig(AppConfig):
    """Register the project package as an application.

    It holds no model anymore, but it must stay installed: its migrations are part
    of the history the lettings and profiles migrations depend on.

    Attributes:
        name (str): the Python path of the application, used in INSTALLED_APPS.
    """
    name = 'oc_lettings_site'
