from django.contrib.syndication.views import Feed
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link

class LatestArtists(Feed):
	title = "Latest tehOrng Artists"
	link = ""
	description = "Updates on changes and additions to Artists."

	def items(self):
		return Artist.objects.filter(is_valid=True).order_by('-created')[:35]

class LatestAlbums(Feed):
	title = "Latest tehOrng Albums"
	link = ""
	description = "Updates on changes and additions to Albums"
	
	def items(self):
		return Album.objects.filter(is_valid=True).order_by('-created')[:35]

class LatestLinks(Feed):
	title = "Latest tehOrng Links"
	link = ""
	description = "Updates on changes and additions to Links"
	
	def items(self):
		return Link.objects.order_by('-created')[:35]
	
	def item_link(self, obj):
		return obj.url

