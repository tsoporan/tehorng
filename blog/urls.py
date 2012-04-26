from django.conf.urls.defaults import *

urlpatterns = patterns('', 
    url(r'^$', 'blog.views.entry_list', name="entry-list"),
    url(r'^archive/(?P<year>\d{4})/$', 'blog.views.entry_archive_year', name="year-archive"),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'blog.views.entry_archive_month', name="month-archive"),
    url(r'^(?P<slug>[-\w]+)/$', 'blog.views.entry_detail', name="entry-detail"),
)
