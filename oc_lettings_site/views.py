"""View of the oc_lettings_site application index."""

import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


# Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque molestie quam lobortis leo
# consectetur ullamcorper non id est. Praesent dictum, nulla eget feugiat sagittis, sem mi
# convallis eros,
# vitae dapibus nisi lorem dapibus sem. Maecenas pharetra purus ipsum, eget consequat ipsum
# lobortis quis. Phasellus eleifend ex auctor venenatis tempus.
# Aliquam vitae erat ac orci placerat luctus. Nullam elementum urna nisi, pellentesque iaculis enim
# cursus in. Praesent volutpat porttitor magna, non finibus neque cursus id.
def index(request):
    """Display the web site welcome page.

    Args:
        request (HttpRequest): the incoming HTTP request.

    Returns:
        HttpResponse: the rendered index welcome page.
    """
    logger.info('Index displayed')
    return render(request, 'index.html')
