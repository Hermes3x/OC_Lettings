"""Views of the lettings application: index and letting."""

from django.shortcuts import get_object_or_404, render
from .models import Letting


# Aenean leo magna, vestibulum et tincidunt fermentum, consectetur quis velit. Sed non placerat
# massa. Integer est nunc, pulvinar a
# tempor et, bibendum id arcu. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices
# posuere cubilia curae; Cras eget scelerisque
def index(request):
    """Display the list of all lettings.

    Args:
        request (HttpRequest): the incoming HTTP request.

    Returns:
        HttpResponse: the rendered list of lettings.
    """
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}

    return render(request, 'lettings/index.html', context)


# Cras ultricies dignissim purus, vitae hendrerit ex varius non. In accumsan porta nisl id
# eleifend. Praesent dignissim, odio eu consequat pretium, purus urna vulputate arcu, vitae
# efficitur
# lacus justo nec purus. Aenean finibus faucibus lectus at porta. Maecenas auctor, est ut luctus
# congue, dui enim mattis enim, ac condimentum velit libero in magna. Suspendisse potenti. In
# tempus a nisi sed laoreet.
# Suspendisse porta dui eget sem accumsan interdum. Ut quis urna pellentesque justo mattis
# ullamcorper ac non tellus. In tristique mauris eu velit fermentum, tempus pharetra est luctus.
# Vivamus consequat aliquam libero, eget bibendum lorem. Sed non dolor risus. Mauris condimentum
# auctor elementum. Donec quis nisi ligula. Integer vehicula tincidunt enim, ac lacinia augue
# pulvinar sit amet.
def letting(request, letting_id):
    """Display a single letting.

    Args:
        request (HttpRequest): the incoming HTTP request.
        letting_id (int): the letting id.

    Returns:
        HttpResponse: the rendered letting.

    Raises:
        Http404: if no letting has this id.
    """
    letting = get_object_or_404(Letting, id=letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)
