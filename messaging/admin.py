from django.contrib import admin
from messaging.models import UserMessage

class UserMessageAdmin(admin.ModelAdmin):
	list_display = ('message', 'from_user', 'to_user', 'read', 'created')

admin.site.register(UserMessage, UserMessageAdmin)

