from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class ReportManager(models.Manager):
    def reports_for_id(self, ctype, id):
        return self.filter(ctype=ctype, object_id=id)  
    
    def reports_for_ctype(self, ctype):
        return self.filter(ctype=ctype)

class Report(models.Model):
    """A generic reporting model for any object."""
    user = models.ForeignKey(User)
    ctype = models.ForeignKey(ContentType, help_text="Relates to a content type.")
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('ctype', 'object_id')
    reason = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    cleared = models.BooleanField(default=False)

    objects = ReportManager()


    class Meta:
        unique_together = ('user', 'ctype', 'object_id',) #user can report object once
        verbose_name = "Reported Item"
        verbose_name_plural = "Reported Items"
    
    def short_reason(self):
        return self.reason[:50]

    #TODO FIX THIS
    def __unicode__(self):
        return str(self.object)  
        #try:
        #    return self.object.name
        #except AttributeError: #name doesn't exist on Link
        #    return self.object.url
