"""Tests of the lettings application: models, URLs and views."""

import pytest
from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed

from lettings import views
from lettings.models import Address, Letting


@pytest.fixture
def letting():
    """Create a letting and its address in the test database.

    Returns:
        Letting: the created letting.
    """
    address = Address.objects.create(
        number=7,
        street='Main Street',
        city='Springfield',
        state='IL',
        zip_code=62701,
        country_iso_code='USA',
    )
    return Letting.objects.create(title='Cozy cabin', address=address)


@pytest.mark.django_db
def test_address_str(letting):
    """An address is displayed as its number followed by its street."""
    assert str(letting.address) == '7 Main Street'


def test_lettings_index_url_resolves_to_index_view():
    """The 'lettings:index' route is /lettings/ and points to the index view."""
    url = reverse('lettings:index')
    assert url == '/lettings/'
    assert resolve(url).func == views.index


def test_letting_url_resolves_to_letting_view():
    """The 'lettings:letting' route is /lettings/<id>/ and points to the letting view."""
    url = reverse('lettings:letting', args=[1])
    assert url == '/lettings/1/'
    assert resolve(url).func == views.letting


@pytest.mark.django_db
def test_lettings_index_view_lists_lettings(client, letting):
    """The lettings page answers 200, uses its template and shows the letting."""
    response = client.get(reverse('lettings:index'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'lettings/index.html')
    assert 'Cozy cabin' in response.content.decode()


@pytest.mark.django_db
def test_letting_view_displays_the_letting(client, letting):
    """The letting page answers 200, uses its template and shows the title."""
    response = client.get(reverse('lettings:letting', args=[letting.id]))
    assert response.status_code == 200
    assertTemplateUsed(response, 'lettings/letting.html')
    assert 'Cozy cabin' in response.content.decode()


@pytest.mark.django_db
def test_letting_view_displays_the_404_error_customized_message(client, letting):
    """An unknown letting answers 404 with the custom 404 page."""
    letting_id = 10000
    response = client.get(reverse('lettings:letting', args=[letting_id]))
    assert response.status_code == 404
    assertTemplateUsed(response, '404.html')
    assert 'does not exist' in response.content.decode()


@pytest.mark.django_db
def test_letting_str(letting):
    """A letting is displayed as its title."""
    assert str(letting) == 'Cozy cabin'
