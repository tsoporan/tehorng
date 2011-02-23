from django.db import models
import datetime
from django.template.defaultfilters import slugify
from tagging.fields import TagField

class Entry(models.Model):
    """A single blog entry."""
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    author = models.CharField(max_length=255)
    body = models.TextField(help_text='Pure HTML is allowed. But use markdown.')
    tags = TagField()
    public = models.BooleanField(help_text="If this is public, else draft.", default=False)
    allow_comments = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('entry-detail', (), {'slug': self.slug})
