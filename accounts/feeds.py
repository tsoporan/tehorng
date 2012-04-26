from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link

class UserArtistFeed(Feed):
    def get_object(self, request, username):
        return get_object_or_404(User, username=username)

    def title(self, obj):
        return "Artist uploads for %s" % obj

    def description(self, obj):
        return "Most recent artist uploads for %s" % obj

    def link(self, obj):
        return "test"

    def items(self, obj):
        return Artist.objects.filter(uploader=obj).order_by('-created')[:50]

class UserAlbumFeed(Feed):
    def get_object(self, request, username):
        return get_object_or_404(User, username=username)

    def title(self, obj):
        return "Album submissions for %s" % obj

    def description(self, obj):
        return "Most recent album submissions for %s" % obj

    def link(self, obj):
        return "test"
        
    def items(self, obj):
        return Album.objects.filter(uploader=obj).order_by('-created')[:50]

    def item_description(self, item):
        return item.artist

class UserLinkFeed(Feed):
    def get_object(self, request, username):
        return get_object_or_404(User, username=username)
        
    def title(self, obj):
        return "Link submissions for %s" % obj

    def description(self, obj):
        return "Most recent link submissions for %s" % obj

    def link(self, obj):
        return "test"
        
    def items(self, obj):
        return Link.objects.filter(uploader=obj).order_by('-created')[:50]
    
    def item_description(self, item):
        return "%s - %s" % (item.album.artist, item.album)
