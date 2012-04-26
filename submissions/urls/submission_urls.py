from django.conf.urls.defaults import *

from submissions.views.artist import artist_list, add_artist, edit_artist, report_artist, delete_artist, artist_detail, addresource_artist, addartwork_artist
from submissions.views.album import add_album, edit_album, report_album, delete_album, album_detail, addresource_album, addartwork_album
from submissions.views.link import add_link, edit_link, report_link, delete_link
from submissions.views.track import manage_tracks

urlpatterns = patterns('', 
    url(r'^$', artist_list, name="artist-index"),
    url(r'^filter/(?P<filter>latest|popular|withalbums|noalbums|withlinks|nolinks)/$', artist_list, name="artist-list-filter"),
    url(r'^letter/(?P<letter>[A-Za-z0-9-]{1,3})/$', artist_list, name="artist-list-letter"),
    url(r'^addartist/$', add_artist, name="add-artist"),
    url(r'^(?P<artist>[-\w]+)/$', artist_detail, name="artist-detail"), 
    url(r'^(?P<artist>[-\w]+)/report/$', report_artist, name="report-artist"), 
    url(r'^(?P<artist>[-\w]+)/edit/$', edit_artist, name="edit-artist"),
    url(r'^(?P<artist>[-\w]+)/delete/$', delete_artist, name="delete-artist"),
    url(r'^(?P<artist>[-\w]+)/addresource/$', addresource_artist, name="addresource-artist"),
    url(r'^(?P<artist>[-\w]+)/addartwork/$', addartwork_artist, name="addartwork-artist"),
)

urlpatterns += patterns('', 
    url(r'^(?P<artist>[-\w]+)/addalbum/$', add_album, name="add-album"),
    url(r'^(?P<artist>[-\w]+)/(?P<album>[-\w]+)/$', album_detail, name="album-detail"),
    url(r'^(?P<artist>[-\w]+)/(?P<album>[-\w]+)/report/$', report_album, name="report-album"), 
    url(r'^(?P<artist>[-\w]+)/(?P<album>[-\w]+)/edit/$', edit_album, name="edit-album"), 
    url(r'^(?P<artist>[-\w]+)/(?P<album>[-\w]+)/delete/$', delete_album, name="delete-album"), 
    url(r'^(?P<artist>[-\w]+)/(?P<album>[-\w]+)/addresource/$', addresource_album, name="addresource-album"), 
    url(r'^(?P<artist>[-\w]+)/(?P<album>[-\w]+)/addartwork/$', addartwork_album, name="addartwork-album"), 
)

urlpatterns += patterns('', 
    url(r'^(?P<artist>[-\w]+)/(?P<album>[-\w]+)/addlink/$', add_link, name="add-link"), 
    url(r'^(?P<artist>[-\w]+)/(?P<album>[-\w]+)/(?P<link>\d+)/report/$', report_link, name="report-link"), 
    url(r'^(?P<artist>[-\w]+)/(?P<album>[-\w]+)/(?P<link>\d+)/edit/$', edit_link, name="edit-link"), 
    url(r'^(?P<artist>[-\w]+)/(?P<album>[-\w]+)/(?P<link>\d+)/delete/$', delete_link, name="delete-link"), 
)
urlpatterns += patterns('', 
    url(r'^(?P<artist>[-\w]+)/(?P<album>[-\w]+)/managetracks/$', manage_tracks, name="manage-tracks"), 
)


