from django.conf.urls.defaults import *
from accounts.feeds import UserArtistFeed, UserAlbumFeed, UserLinkFeed


urlpatterns = patterns('', 
	url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),
	url(r'^register/$', 'accounts.views.register', name="register"),
	#url(r'^register/success/$', 'django.views.generic.simple.direct_to_template', {'template': 'registration/register_success.html'}, name="register-success"),
	#url(r'^verify/(?P<verificationkey>[-\w]+)/$', 'accounts.views.verify', name="verifiy-account"),
	url(r'^profile/$', 'accounts.views.profile', name="profile"),
	url(r'^profile/viewlinks/$', 'accounts.views.view_links', name="view-links"),
	url(r'^profile/viewalbums/$', 'accounts.views.view_albums', name="view-albums"),
	url(r'^profile/viewartists/$', 'accounts.views.view_artists', name="view-artists"),
	url(r'^profile/changeemail/$', 'accounts.views.change_email', name="change-email"),
	url(r'^profile/changepassword/$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change_form.html'}, name="change-password"),
    url(r'^profile/changepassword/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'accounts/password_change_done.html'}),
    url(r'^profile/changeusername/$', 'accounts.views.change_username', name='change-username'),	
	
    url(r'^profile/(?P<username>.*)/viewlinks/$', 'accounts.views.view_links', name='view-links-user'),
    url(r'^profile/(?P<username>.*)/viewalbums/$', 'accounts.views.view_albums', name='view-albums-user'),
    url(r'^profile/(?P<username>.*)/viewartists/$', 'accounts.views.view_artists', name='view-artists-user'),
    
    url(r'^profile/(?P<username>.*)/sendpm/$', 'accounts.views.sendpm_user', name='sendpm-user'),
	url(r'^profile/(?P<username>.*)/report/$', 'accounts.views.report_user', name='report-user'),
	
    #RSS 
    url(r'^profile/(?P<username>.*)/feed/artists/$', UserArtistFeed(), name='user-artist-feed'),
    url(r'^profile/(?P<username>.*)/feed/albums/$', UserAlbumFeed(), name='user-album-feed'),
    url(r'^profile/(?P<username>.*)/feed/links/$', UserLinkFeed(), name='user-link-feed'),
    
    url(r'^profile/(?P<username>.*)/$', 'accounts.views.profile_user', name='profile-user'),
	url(r'^inbox/$', 'accounts.views.inbox', name="inbox"),
	url(r'^inbox/sendpm/$', 'accounts.views.sendpm', name="inbox-sendpm"), 
    url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'accounts/password_reset_form.html'}, name="password-reset"),
	url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'accounts/password_reset_done.html' }),
  url(r'^password-reset/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',{'template_name': 'accounts/password_reset_confirm.html'}),
  url(r'^password-reset/reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'accounts/password_reset_complete.html' }),
	
)
