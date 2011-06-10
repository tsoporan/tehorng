from django.contrib import admin
from accounts.models import UserProfile, OnlineUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'warning', 'created')#'verification_key', 'created') 
	search_fields = ('user__username',)

class OnlineUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'ident', 'updated', 'created')
    search_fields = ('ident',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(OnlineUser, OnlineUserAdmin)
