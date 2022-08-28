import functools

from django.core.exceptions import PermissionDenied
from .models import Place


def user_can_edit_place(function):
    @functools.wraps(function)
    def wrap(request, *args, **kwargs):
        place = Place.objects.get(pk=kwargs['pk'])
        if place.owner == request.user or place.editors.contains(request.user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
