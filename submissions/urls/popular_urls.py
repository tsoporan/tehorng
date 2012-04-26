from django.conf.urls.defaults import *

from submissions.views.popular import popular

urlpatterns = patterns('', 
    url(r'^(?P<ctype>\w+)/(?P<filterby>\w+)/$', popular, name="popular"),
)
