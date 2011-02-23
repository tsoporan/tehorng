from django.conf.urls.defaults import *

urlpatterns = patterns('', 
	url(r'^$', 'contact.views.contact', name="contact"),
    url(r'^success/$', 'django.views.generic.simple.direct_to_template', {'template': 'contact/contact_success.html'}, name='contact-success'),
)
