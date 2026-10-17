"""Profile model of the profiles application."""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """A user profile.

    Attributes:
        user (User): the Django user account this profile belongs to (one profile per user).
        favorite_city (str): the user's favorite city, optional.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """Return the user name.

        Returns:
            str: the user name.
        """
        return self.user.username
