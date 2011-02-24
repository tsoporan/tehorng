from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from tracking.models import TrackedArtist, TrackedAlbum, TrackedLink
from django.contrib.contenttypes.models import ContentType
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link
from datetime import datetime, timedelta
from django.core import serializers
from tracking.signals import hit

def track_artist(request, artist_obj):
    """
    An artist gets tracked when it's page is hit (artist detail)
    this method will only increment the counter for the instance.
    """
    artist = artist_obj
    ctype = ContentType.objects.get(model='artist')
    try:
        trk_obj = TrackedArtist.objects.get(ctype=ctype, object_id=artist.id)
        trk_obj.hits += 1
        trk_obj.save()
    except TrackedArtist.DoesNotExist:
        trk_obj = TrackedArtist(
            ctype = ctype,
            object_id = artist.id,
        )
        if request.user.is_authenticated():
            trk_obj.save()
            trk_obj.users.add(request.user)
        trk_obj.save()

def track_album(request, album_obj):
    """
    An album gets tracked when it's page is hit (album detail)
    this method will only increment the counter for the instance.
    """
    album = album_obj
    ctype = ContentType.objects.get(name='album')
    try:
        trk_obj = TrackedAlbum.objects.get(ctype=ctype, object_id=album.id)
        trk_obj.hits += 1
        trk_obj.save()
    except TrackedAlbum.DoesNotExist:
        trk_obj = TrackedAlbum(
            ctype = ctype,
            object_id = album.id,
        )
        if request.user.is_authenticated():
            trk_obj.save()
            trk_obj.users.add(request.user)
        trk_obj.save()


def track_link(request, object_hash):
    """Track external links."""
    link = get_object_or_404(Link, hash=object_hash)
    #ctype = ContentType.objects.get(name__iexact='link')
    #try to save a tracked object for this link - else - increment counter
    #try:
    #   trk_obj = TrackedLink.objects.get(ctype=ctype, object_id=link.id)
    #   trk_obj.hits += 1 
    #   trk_obj.save()
    #except TrackedLink.DoesNotExist:
    #   trk_obj = TrackedLink(
    #       ctype = ctype,  
    #       object_id = link.id,
    #   )
    #   if request.user.is_authenticated():
    #       trk_obj.save()
    #       trk_obj.users.add(request.user)
    #   trk_obj.save()
    #
    hit.send(sender='track_link', object=link, request=request)
    return HttpResponseRedirect(link.url)


def popular_artists(request, filter=None):
    if not filter: return Http404("No filter provided.")
    if filter == "alltime":
        artists = TrackedArtist.objects.order_by('-hits')[:10]
    if filter == "weekly":
        weekago = datetime.now() - timedelta(days=7)
        now = datetime.now()
        artists = TrackedArtist.objects.order_by('-hits').filter(modified__range=(weekago, now))[:10]
    if filter == "daily":
        dayago = datetime.now() - timedelta(days=1)
        now = datetime.now()
        artists = TrackedArtist.objects.order_by('-hits').filter(modified__range=(dayago, now))[:10]
    
    data = serializers.serialize('json', [artist.object for artist in artists])
    return HttpResponse(data, mimetype="application/javascript")  

def popular_albums(request, filter=None):
    if not filter: return Http404("No filter provided.")
    if filter == "alltime":
        albums = TrackedAlbum.objects.order_by('-hits')[:10]
    if filter == "weekly":
        weekago = datetime.now() - timedelta(days=7)
        now = datetime.now()
        albums = TrackedAlbum.objects.order_by('-hits').filter(modified__range=(weekago, now))[:10]
    if filter == "daily":
        dayago = datetime.now() - timedelta(days=1)
        now = datetime.now()
        albums = TrackedAlbum.objects.order_by('-hits').filter(modified__range=(dayago, now))[:10]

    data = serializers.serialize('json', [album.object for album in albums])
    return HttpResponse(data, mimetype="application/javascript")  

def popular_links(request, filter=None):
    if not filter: return Http404("No filter provided.")
    if filter == "alltime":
        links = TrackedLink.objects.order_by('-hits')[:10]
    if filter == "weekly":
        weekago = datetime.now() - timedelta(days=7)
        now = datetime.now()
        links = TrackedLink.objects.order_by('-hits').filter(modified__range=(weekago, now))[:10]
    if filter == "daily":
        dayago = datetime.now() - timedelta(days=1)
        now = datetime.now()
        links = TrackedLink.objects.order_by('-hits').filter(modified__range=(dayago, now))[:10]
    
    data = serializers.serialize('json', [link.object for link in links])
    return HttpResponse(data, mimetype="application/javascript")  

