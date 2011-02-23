from django.contrib.sitemaps import Sitemap
from blog.models import Entry

class EntrySitemap(Sitemap):
	changefreq = "never"
	priority = 0.5

	def items(self):
		return Entry.objects.all()
	
	def lastmod(self, obj):
		return obj.created
