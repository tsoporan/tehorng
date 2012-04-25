from django.views.generic import list_detail
from tagging.models import Tag, TaggedItem
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from submissions.models.artist import Artist
from submissions.models.album import Album
from blog.models import Entry
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import cache_page

def tag_list(request, filter=None):
	"""
	View to display a list of tags.
	Returns a queryset with special context variables to build a tag cloud based by filter.
	"""
	
	if filter == 'albums':
		queryset = Tag.objects.cloud_for_model(Album, steps=20, min_count=2)
	elif filter == 'blogs':
		queryset = Tag.objects.cloud_for_model(Entry, steps=20)
	else:
		queryset = Tag.objects.cloud_for_model(Artist, steps=20, min_count=2)

	return render_to_response('tagging/tag_list.html', {
		'filter': filter,
		'tag_list': queryset,
	}, context_instance=RequestContext(request))

def tag_detail(request, filter, tag):
	"""
	View that displays the detailed tag.
	"""
	tag = get_object_or_404(Tag, id=tag)
	if filter == 'artists':
		taggeditems = TaggedItem.objects.filter(content_type=ContentType.objects.get_for_model(Artist), tag=tag)
	elif filter == 'albums':
		taggeditems = TaggedItem.objects.filter(content_type=ContentType.objects.get_for_model(Album), tag=tag)
	elif filter == 'blogs':
		taggeditems = TaggedItem.objects.filter(content_type=ContentType.objects.get_for_model(Entry), tag=tag)
	else:
		taggeditems = TaggedItem.objects.all()		

	return render_to_response('tagging/tag_detail.html', {
		'filter': filter,
		'tag': tag,
		'taggeditems': taggeditems,
	}, context_instance=RequestContext(request))
