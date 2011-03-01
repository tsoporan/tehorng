from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse

from submissions.views.utils import get_popular
from django.contrib.contenttypes.models import ContentType
import os
from django.conf import settings

def popular(request, ctype, filterby, template="submissions/popular/popular_load.html"):
    popular_list = get_popular(ctype=ctype, filterby=filterby.lower(), num=10)

    return render_to_response(template, {
        'ctype': ctype,
        'filterby': filterby,
        'objects': popular_list,
    })
