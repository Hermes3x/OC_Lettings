"""Tests of the project: home page and error pages."""

from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed
from oc_lettings_site import views

from django.views.defaults import server_error


def test_custom_500_page(rf):
    """The server error handler answers 500 with the custom 500 page."""
    response = server_error(rf.get('/'))
    assert response.status_code == 500
    assert 'Something went wrong' in response.content.decode()


def test_home_url_resolves_to_index_view():
    """The 'index' route is / and points to the home page view."""
    url = reverse('index')
    assert url == '/'
    assert resolve(url).func == views.index


def test_home_index_view_response_is_200(client):
    """The home page answers 200, uses its template and shows the welcome title."""
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'index.html')
    assert 'Welcome to your Holiday Homes' in response.content.decode()


def test_home_url_view_displays_the_404_error_customized_message(client):
    """An unknown address answers 404 with the custom 404 page."""
    response = client.get('/nimporte-quoi/')
    assert response.status_code == 404
    assertTemplateUsed(response, '404.html')
    assert 'does not exist' in response.content.decode()
