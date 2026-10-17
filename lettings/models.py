"""Models of the lettings application: addresses and lettings."""

from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    """A postal address of a property for rent.

    Attributes:
        number (int): the street number, up to 9999.
        street (str): the street name.
        city (str): the city.
        state (str): the two-letter state code.
        zip_code (int): the postal code, up to 99999.
        country_iso_code (str): the three-letter ISO country code.
    """

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    class Meta:
        """Model options: the plural name shown in the admin."""

        verbose_name_plural = 'Addresses'

    def __str__(self):
        """Return the text used to display an address.

        Returns:
            str: the street number followed by the street name.
        """

        return f'{self.number} {self.street}'


class Letting(models.Model):
    """A property for rent, with its title and address.

    Attributes:
        title (str): the title of the letting up to 256 characters.
        address (Address): the address of the property.
    """
    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        """Return the text used to display a letting.

        Returns:
            str: the letting's title.
        """
        return self.title
