from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link

from datetime import datetime, timedelta
from django.core import serializers

from tracking.models import Hit

def get_popular(ctype, filterby="hourly"):
    try:
        ct = ContentType.objects.get(name=ctype)
    except:
        return

    now = datetime.now()
    hits = Hit.objects.all()

    if filterby == "hourly":
        hourago = now - timedelta(hours=1)
        results = hits.filter(content_type=ct, timestamp__range=(hourago, now))

    elif filterby == "daily":
        dayago = now - timedelta(days=1)
        results = hits.filter(content_type=ct, timestamp__range(dayago, now))

    elif filterby == "monthly":
        monthago = now - timedelta(days=30)
        results = hits.filter(content_type=ct, timestamp__range(monthago, now))

    else: #all results
        results = hits.filter(content_type=ct)

    return serializers.serialize('json', results)       



