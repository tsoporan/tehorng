from django.contrib import admin
from reporting.models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'reason', 'ctype', 'user', 'created')

admin.site.register(Report, ReportAdmin)
