from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse

from submissions.views.utils import get_popular
from django.contrib.contenttypes.models import ContentType

def popular(request, ctype, filterby):
    content_type = get_object_or_404(ContentType, name__iexact=ctype)
    json = get_popular(ctype=content_type, filterby=filterby.lower())

    return HttpResponse(
        json, 
        content_type = 'application/javascript; charset=utf8'
    )
