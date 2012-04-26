from django.conf.urls.defaults import *
from reporting.views import report_object

urlpatterns = patterns('', 
    url('^(?P<ctype>\w+)/(?P(object_id)\d+)/$', report_object, name="report-object"),
)
