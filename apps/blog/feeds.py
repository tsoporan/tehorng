from django.contrib.syndication.feeds import Feed
from blog.models import Entry

class LatestEntries(Feed):
	title = "Latest tehOrng blog entries."
	link = ""
	description = "Updates on changes and additions to Entries"

	def items(self):
		return Entry.objects.order_by('-created')[:35]
