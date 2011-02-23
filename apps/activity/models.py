"""
A way to represent user activity. Activity should be measured by an action. Currently tehorng is limited to CRUD type functionality.
For example, a user adding an artist would be considerd an action, along with editing and deleting.
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import datetime

class Action(models.Model):
    ACTION_TYPE = (
        ('Add', 'Add'), 
        ('Edit', 'Edit'), 
        ('Remove', 'Remove'), 
    )
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(User)
    action = models.CharField(max_length=50, choices=ACTION_TYPE) 
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return "%s for %s on %s" % (self.action, self.user.username, self.content_object)
