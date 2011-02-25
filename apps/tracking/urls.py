from django.conf.urls.defaults import *
from tracking import views
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('', 
    url(r'^topbar/$', direct_to_template,  {'template': 'submissions/topbar.html'}, name="topbar"),
    url(r'^(?P<object_hash>\w+)/$', views.track_link, name="track-link"),
)
