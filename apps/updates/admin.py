from django.contrib import admin
from updates.models import Update

class UpdateAdmin(admin.ModelAdmin):
	list_display = ('message','created','expires', 'expired')
	
admin.site.register(Update, UpdateAdmin)

