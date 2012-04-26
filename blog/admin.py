from django.contrib import admin
from blog.models import Entry

class EntryAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'author', 'created', 'public')
	search_fields = ('title',)

admin.site.register(Entry, EntryAdmin)
