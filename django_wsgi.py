import os, sys
import django.core.handlers.wsgi

sys.path.append('/home/tsoporan/tehorng_env')

os.environ['DJANGO_SETTINGS_MODULE'] = 'tehorng.settings'

application = django.core.handlers.wsgi.WSGIHandler()

applications = {'/': 'application'} 
