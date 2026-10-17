"""Tests of the profiles application: models, URLs and views."""

import pytest

from django.contrib.auth.models import User
from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed
from profiles.models import Profile
from profiles import views


@pytest.fixture
def profile():
    """Create a user and his profile in the test database.

    Returns:
        Profile: the created profile.
    """
    user = User.objects.create_user(username='jdoe', password='secret')
    return Profile.objects.create(user=user, favorite_city='Paris')


@pytest.mark.django_db
def test_profile_str(profile):
    """A profile is displayed as its user's username."""
    assert str(profile) == 'jdoe'


def test_profiles_url_resolve_to_profiles_index_view():
    """The 'profiles:index' route is /profiles/ and points to the index view."""
    url = reverse('profiles:index')
    assert url == '/profiles/'
    assert resolve(url).func == views.index


def test_profile_url_resolves_to_profile_view():
    """The 'profiles:profile' route is /profiles/<username>/ and points to the profile view."""
    url = reverse('profiles:profile', args=['jdoe'])
    assert url == '/profiles/jdoe/'
    assert resolve(url).func == views.profile


@pytest.mark.django_db
def test_profiles_index_view_lists_profiles(client, profile):
    """The profiles page answers 200, uses its template and lists the user."""
    response = client.get(reverse('profiles:index'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'profiles/index.html')
    assert 'jdoe' in response.content.decode()


@pytest.mark.django_db
def test_profile_view_displays_the_favorite_user_city(client, profile):
    """The profile page answers 200, uses its template and shows the user's favorite city."""
    response = client.get(reverse('profiles:profile', args=[profile.user.username]))
    assert response.status_code == 200
    assertTemplateUsed(response, 'profiles/profile.html')
    assert 'Paris' in response.content.decode()


@pytest.mark.django_db
def test_profile_view_displays_the_404_error_customized_message(client):
    """An unknown profile answers 404 with the custom 404 page."""
    response = client.get(reverse('profiles:profile', args=['unknown']))
    assert response.status_code == 404
    assertTemplateUsed(response, '404.html')
    assert 'does not exist' in response.content.decode()
