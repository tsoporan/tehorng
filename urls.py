from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

#search 
from search.views import OrngSearchView
from haystack.forms import SearchForm

#sitemaps
from submissions.sitemaps import ArtistSitemap, AlbumSitemap
from django.contrib.sitemaps import FlatPageSitemap
from blog.sitemaps import EntrySitemap

sitemaps = {
   'artists': ArtistSitemap,
   'albums': AlbumSitemap,
   'pages': FlatPageSitemap,
   'entries': EntrySitemap,
}

#rss 
from submissions.feeds import LatestArtists, LatestAlbums, LatestLinks
from blog.feeds import LatestEntries

feeds = {
   'artists': LatestArtists,
   'albums': LatestAlbums,
   'links': LatestLinks,
   'entries': LatestEntries,
}

urlpatterns = patterns('',
    url(r'^$', 'tehorng.views.index', name="index"),
    #tehorng irc -- just a simple redirect to port 9090 where qwebirc is running
    url(r'^irc/$', 'django.views.generic.simple.redirect_to', {'url': 'http://tehorng.com:9090'}),

    #submissions
    (r'^artists/', include('submissions.urls')),
    
    #tag specific
    url(r'^tags/$', 'submissions.views.tag.tag_list', name="tag-index"),
    url(r'^tags/(?P<filter>artists|albums|blogs)/$','submissions.views.tag.tag_list', name="tag-list"),
    url(r'^tags/(?P<filter>artists|albums|blogs)/(?P<tag>\d+)/$', 'submissions.views.tag.tag_detail', name="tag-detail"),

    #polls
    url(r'^polls/', include('polls.urls')),

    #auth
    (r'^accounts/', include('accounts.urls')),
    
    #search
    url(r'^search/', include('search.urls'), name="search"),

    #comments - handle deleteing/flagging in submissiosn
    url(r'^comments/flagcomment/(?P<id>\d+)/$', 'submissions.comments.flag_comment', name="flag-comment"), 
    url(r'^comments/deletecomment/(?P<id>\d+)/$', 'submissions.comments.delete_comment', name="delete-comment"), 
    (r'^comments/', include('django.contrib.comments.urls')),

    #blog
    (r'^blog/', include('blog.urls')),

    #contact
    (r'^contact/', include('contact.urls')),

    #tracking
    (r'^view/', include('tracking.urls')),

    #rss
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),

    #sitemaps
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    #robots
    (r'^robots.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt'}),

    #admin
    (r'^admin/', include(admin.site.urls)),

    #sentry
    (r'^sentry/', include('sentry.urls')),

    ### Seriving static media with django 
    ### NOTE: this is for development ONLY, strongly encouranged to use a seperate server to handle static content
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    ###

    #flatpage fallback
    (r'^', include('django.contrib.flatpages.urls')),

)
