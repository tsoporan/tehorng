from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link

from datetime import datetime, timedelta

from tracking.models import Hit

from collections import Counter

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

import pickle
import json

def get_popular(ctype="artist", filterby="hourly"):
    try:
        ct = ContentType.objects.get(name__iexact=ctype)
    except:
        return
    
    counter = Counter()
    now = datetime.now()
    hits = Hit.objects.all()

    loads = pickle.loads
    dumps = pickle.dumps

    if filterby == "hourly":
        counter.clear()
    
        if cache.has_key('popular_hourly'):
            results = loads(cache.get('popular_hourly'))
        else:
            hourago = now - timedelta(hours=1)
            hits = hits.filter(content_type=ct, timestamp__range=(hourago, now))
            for obj in hits:
                counter[obj.content_object] += 1                        
            results = counter.most_common()[:20]
            cache.set('popular_hourly', dumps(results), 60*60) #cache for an hour

    elif filterby == "daily":
        counter.clear()
        dayago = now - timedelta(days=1)
        
        if cache.has_key('popular_daily'):
            results = loads(cache.get('popular_daily'))
        else:
            hits  = hits.filter(content_type=ct, timestamp__range=(dayago, now))
            for obj in hits:
                counter[obj.content_object] += 1                        
            results = counter.most_common()[:20]
            cache.set('popular_daily', dumps(results), 60*60*24) #cache for a day

    elif filterby == "monthly":
        counter.clear()
        monthago = now - timedelta(days=30)
        
        if cache.has_key('popular_monthly'):
            results = loads(cache.get('popular_monthly'))
        else:
            hits = hits.filter(content_type=ct, timestamp__range=(monthago, now))
            for obj in hits: 
                counter[obj.content_object] += 1                        
            results = counter.most_common()[:20]
            cache.set('popular_monthly', dumps(results), 60*60*24*30) #cache for month

    else: #all results
        counter.clear()
 
        if cache.has_key('popular_alltime'):
            results = pickle.loads(cache.get('popular_alltime'))
        else:
            hits = hits.filter(content_type=ct)
            for obj in hits:
                counter[obj.content_object] += 1                        
            results = counter.most_common()[:20]
            cache.set('popular_alltime', pickle.dumps(results), 60*60*24*30) #cache for month


    return json.dumps([r[0].name for r in results])
