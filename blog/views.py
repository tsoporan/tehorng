from django.views.generic import list_detail
from blog.models import Entry
from django.template import RequestContext
from django.shortcuts import render_to_response
import datetime
from django.views.decorators.cache import cache_page

YEARS = Entry.objects.dates('created', 'year')
MONTHS = Entry.objects.dates('created', 'month')

def entry_list(request):
    years = Entry.objects.filter(public=True).dates('created', 'year')
    months = Entry.objects.filter(public=True).dates('created', 'month')
    return list_detail.object_list(
        request,
        queryset = Entry.objects.filter(public=True)[:10], #only show 10
        template_object_name = 'entry',
        extra_context = {
            'years': years,
            'months': months,
        }
    )

def entry_detail(request, slug):
    years = Entry.objects.filter(public=True).dates('created', 'year')
    months = Entry.objects.filter(public=True).dates('created', 'month')
    return list_detail.object_detail(
        request,
        queryset = Entry.objects.filter(public=True),
        slug = slug,
        template_object_name = 'entry',
        extra_context = {
            'years':years, 
            'months': months,
        }
    )

def entry_archive_year(request, year):
    entries = Entry.objects.filter(created__year=year, public=True)
    return render_to_response('blog/year_archive.html', {
        'year': year,
        'entries': entries,
    }, context_instance=RequestContext(request))

def entry_archive_month(request, year, month):
    entries = Entry.objects.filter(created__year=year, created__month=month, public=True)
    return render_to_response('blog/month_archive.html', {
        'year': year,
        'month': datetime.date(int(year), int(month), 1),
        'entries': entries,
    }, context_instance=RequestContext(request))
