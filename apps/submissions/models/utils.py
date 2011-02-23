import string
from django.utils.hashcompat import sha_constructor
from django.template.defaultfilters import slugify
import os
import time
from django.conf import settings

SALT = getattr(settings, 'HASH_TRACKING_SALT')

def strip_punc(s):
	"""Takes a string and strips its punctution returning the clean string."""
	_string = s
	punc = set(string.punctuation)
	return ''.join([ch for ch in _string if ch not in punc])

def gen_hash(object_url):
	"""
	Generate a hash object of objectid+salt.
	""" 
	return sha_constructor(str(object_url+str(time.time()))+SALT).hexdigest()

def get_artist_path(instance, filename):
	return os.path.join('artists', slugify(instance.name), filename)

def get_album_path(instance, filename):
	return os.path.join('albums', slugify(instance.name), filename)


