"""Views of the profiles application: index and profile."""

import logging

from django.http import Http404
from django.shortcuts import render

from .models import Profile

logger = logging.getLogger(__name__)


# Sed placerat quam in pulvinar commodo. Nullam laoreet consectetur ex, sed consequat libero
# pulvinar eget. Fusc
# faucibus, urna quis auctor pharetra, massa dolor cursus neque, quis dictum lacus d
def index(request):
    """Display the list of all profiles.

    Args:
        request (HttpRequest): the incoming HTTP request.

    Returns:
        HttpResponse: the rendered list of profiles.
    """
    profiles_list = Profile.objects.all()
    logger.info('Profiles list displayed: %s profiles.', len(profiles_list))
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


# Aliquam sed metus eget nisi tincidunt ornare accumsan eget lac
# laoreet neque quis, pellentesque dui. Nullam facilisis pharetra vulputate. Sed tincidunt, dolor
# id facilisis fringilla, eros leo tristique lacus,
# it. Nam aliquam dignissim congue. Pellentesque habitant morbi tristique senectus et netus et
# males
def profile(request, username):
    """Display a user profile.

    Args:
        request (HttpRequest): the incoming HTTP request.
        username (str): the username of the profile to display.

    Returns:
        HttpResponse: the rendered profile.

    Raises:
        Http404: if no user has this username.
    """
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        logger.warning('Profile %s not found.', username)
        raise Http404('Profile not found')
    logger.info('Profile %s displayed.', username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
