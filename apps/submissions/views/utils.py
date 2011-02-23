from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db import connection
from django.core import serializers
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link
from tagging.models import Tag, TaggedItem

@login_required
def delete_confirm(request, obj):
	"""
	A general delete_confirm function that relies on the "obj" passed in to determine next course of action. 
	"""
	if isinstance(obj, Artist):
		artist = obj
		if request.method == 'POST' and 'yes' in request.POST:
			messages.success(request, "\"%s\" deleted." % (artist.name,))
			artist.delete()
			return HttpResponseRedirect(reverse('artist-index'))
		elif request.method == 'POST' and 'no' in request.POST:
			return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))

	if isinstance(obj, Album):
		album = obj
		artist = album.artist
		if request.method == 'POST' and 'yes' in request.POST:
			messages.success(request, "\"%s\" deleted." % (album.name,))
			album.delete()
			return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))
		elif request.method == 'POST' and 'no' in request.POST:
			return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
	
	if isinstance(obj, Link):
		link = obj
		album = link.album
		artist = album.artist
		if request.method == 'POST' and 'yes' in request.POST:
			messages.success(request, "\"%s\" deleted." % (link,))
			link.delete()
			return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
		elif request.method == 'POST' and 'no' in request.POST:
			return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
	
	return render_to_response('tehorng/delete_confirm.html', locals(), context_instance=RequestContext(request))

def autocomplete_data(request):
	results = "" 
	if 'q' in request.GET and request.method == 'GET':
		query = request.GET['q']
		limit = request.GET['limit']
		if len(query) > 1:
			query = '%'+query+'%'
			cursor = connection.cursor()
			cursor.execute("SELECT name FROM submissions_artist WHERE name LIKE %s UNION SELECT name FROM submissions_album WHERE name LIKE %s UNION SELECT title FROM submissions_track WHERE title LIKE %s", (query,query,query))
			results = "\n".join([object[0] for object in cursor.fetchall()][:int(limit)])
	#json = simplejson.dumps(results)
	#return HttpResponse(json, mimetype='application/json')
	return HttpResponse(results)

