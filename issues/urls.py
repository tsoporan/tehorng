from django.conf.urls.defaults import *
from issues import views

urlpatterns = patterns('', 
    url(r'^$', views.issues_list, name='issues-list'),
    url(r'^create/$', views.create_issue, name='create-issue'),
    url(r'^(?P<issue_id>\d+)/$', views.issue_detail, name='issue-detail'), 
)
