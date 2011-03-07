from django.db import models

class Query(models.Model):
    text = models.TextField()
    hits = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    last_hit = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text[:20]
