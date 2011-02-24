from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


STATUS_CHOICES = (
    (1, 'Open'),
    (2, 'Working'),
    (3, 'Closed'),
)

PRIORITY_CHOICES = (
    (1, 'Very High'),
    (2, 'High'),
    (3, 'Moderate'),
    (4, 'Low'), 
    (5, 'Very Low')
)

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    submitter = models.ForeignKey(User)
    description = models.TextField(blank=True)
    status = models.IntegerField(default=1, choices=STATUS_CHOICES)
    priority = models.IntegerField(default=3, choices=PRIORITY_CHOICES)

    class Meta:
        ordering = ['status', 'priority', 'pub_date', 'title']

    def __unicode__(self):
        return self.title
