from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db import connection
from django.core import serializers
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link
from tagging.models import Tag, TaggedItem
from activity.signals import delete_object
import inspect
from datetime import datetime, timedelta

from tracking.models import Hit

from collections import Counter, OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

import pickle
import json


def autocomplete_data(request):
    results = "" 
    if 'q' in request.GET and request.method == 'GET':
        query = request.GET['q']
        limit = request.GET['limit']
        if len(query) > 1:
            query = '%'+query+'%'
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM submissions_artist WHERE name LIKE %s UNION SELECT name FROM submissions_album WHERE name LIKE %s UNION SELECT title FROM submissions_track WHERE title LIKE %s", (query,query,query))
            results = "\n".join([object[0] for object in cursor.fetchall()][:int(limit)])
    #json = simplejson.dumps(results)
    #return HttpResponse(json, mimetype='application/json')
    return HttpResponse(results)

def get_popular(ctype, filterby, num=20):
    ct = ContentType.objects.get(name__iexact=ctype)
    now = datetime.now()

    loads = pickle.loads
    dumps = pickle.dumps

    norm_sql =  "select * from (select object_id,content_type_id,count(*) from tracking_hit group by object_id, content_type_id) as foo WHERE content_type_id = %s \
                 order by count desc limit 20"
    
    range_sql = "select * from (select object_id,content_type_id,count(*) from tracking_hit where timestamp between %s and %s \
                 group by object_id, content_type_id) as foo WHERE content_type_id = %s order by count desc limit 20"
        
    def get_results(sql, ctype, start_date=None, end_date=None):
        cursor = connection.cursor()
        if start_date and end_date:
            cursor.execute(sql, [start_date, end_date, ctype.id])
        else:
            cursor.execute(sql, [ct.id])
        fetched = cursor.cursor.fetchall()
        return [(ctype.model_class().objects.get(id=result[0]), result[2]) for result in fetched] 

    if filterby == "hourly":
        hourago = now - timedelta(hours=1) 
        cache_key = 'popular_hourly_%s' % ctype 
        if cache.has_key(cache_key):
            results = loads(cache.get(cache_key))
        else:
            results = get_results(range_sql, ct, hourago, now) 
            cache.set(cache_key, dumps(results), 60*60) #cache for an hour 
    
    elif filterby == "daily":
        dayago = now - timedelta(days=1)
        cache_key = 'popular_daily_%s' % ctype 
        if cache.has_key(cache_key):
            results = loads(cache.get(cache_key))
        else:
            results = get_results(range_sql, ct, dayago, now) 
            cache.set(cache_key, dumps(results), 60*60*24) #cache for a day

    elif filterby == "weekly":
        weekago = now - timedelta(days=7)
        cache_key = 'popular_weekly_%s' % ctype

        if cache.has_key(cache_key):
            results = loads(cache.get(cache_key))
        else:
            results = get_results(range_sql, ct, weekago, now)
            cache.set(cache_key, dumps(results), 60*60*24) #cache for a day

    elif filterby == "monthly":
        monthago = now - timedelta(days=30)
        cache_key = 'popular_monthly_%s' % ctype 

        if cache.has_key(cache_key):
            results = loads(cache.get(cache_key))
        else:
            results = get_results(range_sql, ct, monthago, now)
            cache.set(cache_key, dumps(results), 60*60*24) #cache for a day

    else: #all results
        cache_key = 'popular_alltime_%s' % ctype 

        if cache.has_key(cache_key):
           results = pickle.loads(cache.get(cache_key))
        else:
            results = get_results(norm_sql, ct)
            cache.set(cache_key, pickle.dumps(results), 60*60*24) #cache for a day

    return results
