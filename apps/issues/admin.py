from django.contrib import admin
from issues.models import Issue

class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'mod_date', 'submitter', 'description', 'status', 'priority')

admin.site.register(Issue, IssueAdmin)
