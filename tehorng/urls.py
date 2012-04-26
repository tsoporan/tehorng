from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from submissions.sitemaps import ArtistSitemap, AlbumSitemap
from django.contrib.sitemaps import FlatPageSitemap
from blog.sitemaps import EntrySitemap

sitemaps = {
   'artists': ArtistSitemap,
   'albums': AlbumSitemap,
   'pages': FlatPageSitemap,
   'entries': EntrySitemap,
}

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
    url(r'^artists/', include('submissions.urls.submission_urls')),
    url(r'^popular/', include('submissions.urls.popular_urls')),
    url(r'^tags/$', 'submissions.views.tag.tag_list', name="tag-index"),
    url(r'^tags/(?P<filter>artists|albums|blogs)/$','submissions.views.tag.tag_list', name="tag-list"),
    url(r'^tags/(?P<filter>artists|albums|blogs)/(?P<tag>\d+)/$', 'submissions.views.tag.tag_detail', name="tag-detail"),
    url(r'^polls/', include('polls.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^issues/', include('issues.urls')),
    url(r'^comments/flagcomment/(?P<id>\d+)/$', 'submissions.comments.flag_comment', name="flag-comment"), 
    url(r'^comments/deletecomment/(?P<id>\d+)/$', 'submissions.comments.delete_comment', name="delete-comment"), 
    url(r'^comments/', include('django.contrib.comments.urls')),
    #url(r'^blog/', include('blog.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^view/', include('tracking.urls')),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.Feed', {'feed_dict': feeds}),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^robots.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^vote/', include('voting.urls')),
    url(r'^forum/', include('forum.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,    
        }),
    )

#catch-all must be last
urlpatterns += patterns('', 
    url(r'', include('django.contrib.flatpages.urls')),        
)



