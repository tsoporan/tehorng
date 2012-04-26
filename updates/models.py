from django.db import models
import datetime

class Update(models.Model):
    message = models.TextField()
    created = models.DateTimeField(default=datetime.datetime.now, editable=False)
    expires = models.DateTimeField()
    expired = models.BooleanField(default=False)

    def __unicode__(self):
        return self.message

