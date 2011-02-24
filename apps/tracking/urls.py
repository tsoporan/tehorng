from django.conf.urls.defaults import *
from tracking.views import track_link, popular_artists, popular_albums, popular_links

urlpatterns = patterns('', 
    url(r'^(?P<object_hash>\w+)/$', track_link, name="track-link"),
    url(r'^artists/popular/(?P<filter>alltime|weekly|daily)/$', popular_artists, name="popular-artists"),
    url(r'^albums/popular/(?P<filter>alltime|weekly|daily)/$', popular_albums, name="popular-albums"),
    url(r'^links/popular/(?P<filter>alltime|weekly|daily)$', popular_links ,name="popular-links"),
)
