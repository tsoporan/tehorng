from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link
from submissions.models.track import Track
from tagging.models import Tag
from tracking.models import TrackedArtist, TrackedAlbum, TrackedLink
from django.contrib.auth.models import User
from django.db.models import Count
from haystack.forms import SearchForm
from django.views.decorators.cache import cache_page
import datetime
from updates.models import Update


def index(request):
    tracked = TrackedArtist.objects.order_by('-hits')[:20]
    t_artists= [artist for artist in tracked if artist.object.is_public][:10]

    now = datetime.datetime.now()
    for update in Update.objects.filter(expired=False):
        if update.expires < now:
            update.expired = True
            update.save()

    context = RequestContext(request, {
        'updates': Update.objects.filter(expired=False),
        'artist_count': Artist.objects.count(),
        'album_count' : Album.objects.count(),
        'link_count' : Link.objects.count(),
        'tag_count' : Tag.objects.count(),
        'user_count' : User.objects.count(),
        'track_count': Track.objects.count(),
        'latest_artists' : Artist.objects.filter(is_valid=True, is_deleted=False).order_by('-created')[:10],
        'latest_albums' : Album.objects.filter(is_valid=True, is_deleted=False).order_by('-created')[:10],
        'latest_links' : Link.objects.order_by('-created').filter(is_deleted=False)[:10],
        'popular_artists' : t_artists,
        'popular_albums' : TrackedAlbum.objects.order_by('-hits')[:10],
        'popular_links' : TrackedLink.objects.order_by('-hits')[:10],
        'top_contrib_artists': User.objects.annotate(Count('artist')).order_by('-artist__count')[1:11], #get rid of tehorng
        'top_contrib_albums': User.objects.annotate(Count('album')).order_by('-album__count')[1:11], #get rid of tehorng
        'top_contrib_links': User.objects.annotate(Count('link')).order_by('-link__count')[:10],
        'form' : SearchForm(initial={'q': "artist, album, or song"}),
    })
    return render_to_response('tehorng/index.html', context)
