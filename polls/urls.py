from django.conf.urls.defaults import *

urlpatterns = patterns('', 
    url(r'^$', 'polls.views.index', name='poll-index'),
    url(r'^(?P<poll_id>\d+)/$', 'polls.views.detail', name='poll-detail'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote', name='poll-vote'),
    url(r'^(?P<poll_id>\d+)/results/$', 'polls.views.results', name='poll-results'),
)
