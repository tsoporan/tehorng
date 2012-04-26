from django.contrib import admin
from polls.models import Poll, Choice, Feedback

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 1

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline, FeedbackInline]
    list_display = ['question', 'type', 'created']
    list_filter = ['created', 'type']
    search_fields = ['question']
    date_hierarchy = 'created'


admin.site.register(Poll, PollAdmin)
