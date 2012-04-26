from django.conf.urls.defaults import *
from voting.views import vote_on_object
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link

artist_dict =  {'model': Artist, 'template_object_name': 'artist', 'allow_xmlhttprequest': True}
album_dict =  {'model': Album, 'template_object_name': 'album', 'allow_xmlhttprequest': True}
link_dict =  {'model': Link, 'template_object_name': 'link', 'allow_xmlhttprequest': True}

urlpatterns = patterns('',
    url(r'^artist/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, artist_dict, name="vote-artist-object"),
    url(r'^album/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, album_dict,  name="vote-album-object"),
    url(r'^link/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, link_dict, name="vote-link-object"),
)

