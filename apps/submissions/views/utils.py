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
    ct = ctype 
    counter = Counter()
    now = datetime.now()
    hits = Hit.objects.all()

    loads = pickle.loads
    dumps = pickle.dumps

    if filterby == "hourly":
        counter.clear()
        cache_key = 'popular_hourly_%s' % ctype 
        if cache.has_key(cache_key):
            results = loads(cache.get(cache_key))
        else:
            hourago = now - timedelta(hours=1)
            hits = hits.filter(content_type=ct, timestamp__range=(hourago, now))
            for obj in hits:
                counter[obj.content_object] += 1                        
            results = counter.most_common()[:num]
            cache.set(cache_key, dumps(results), 60*60) #cache for an hour

    elif filterby == "daily":
        counter.clear()
        dayago = now - timedelta(days=1)
        cache_key = 'popular_daily_%s' % ctype 
        if cache.has_key(cache_key):
            results = loads(cache.get(cache_key))
        else:
            hits  = hits.filter(content_type=ct, timestamp__range=(dayago, now))
            for obj in hits:
                counter[obj.content_object] += 1                        
            results = counter.most_common()[:num]
            cache.set(cache_key, dumps(results), 60*60*24) #cache for a day

    elif filterby == "weekly":
        counter.clear()
        weekago = now - timedelta(days=7)
        cache_key = 'popular_weekly_%s' % ctype

        if cache.has_key(cache_key):
            results = loads(cache.get(cache_key))
        else:
            hits = hits.filter(content_type=ct, timestamp__range=(weekago, now))
            for obj in hits:
                counter[obj.content_object] += 1
            results = counter.most_common()[:num]
            cache.set(cache_key, dumps(results), 60*60*24*7) #cache for a week

    elif filterby == "monthly":
        counter.clear()
        monthago = now - timedelta(days=30)
        cache_key = 'popular_monthly_%s' % ctype 

        
        if cache.has_key(cache_key):
            results = loads(cache.get(cache_key))
        else:
            hits = hits.filter(content_type=ct, timestamp__range=(monthago, now))
            for obj in hits: 
                counter[obj.content_object] += 1                        
            results = counter.most_common()[:num]
            cache.set(cache_key, dumps(results), 60*60*24*30) #cache for month

    else: #all results
        counter.clear()
        cache_key = 'popular_alltime_%s' % ctype 
 
        if cache.has_key(cache_key):
           results = pickle.loads(cache.get(cache_key))
        else:
            hits = hits.filter(content_type=ct)
            for obj in hits:
                counter[obj.content_object] += 1                        
            results = counter.most_common(num)
            cache.set(cache_key, pickle.dumps(results), 60*60*24*30) #cache for month

    rdict = dict([(r[0], r[1]) for r in results])
    odict = OrderedDict(sorted(rdict.items(), key=lambda i: i[1], reverse=True))
    return odict
