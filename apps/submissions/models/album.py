from django.db import models
from submissions.models.utils import strip_punc, get_album_path
from django.template.defaultfilters import slugify
from submissions.managers import AlbumManager
from django.contrib.auth.models import User
from submissions.models.artist import Artist
from tagging.fields import TagField
from tracking.models import TrackedAlbum
from django.contrib.contenttypes.models import ContentType

class Album(models.Model):
    """
    A single album that is unique for an artist.
    """
    name = models.CharField('name', max_length=255, help_text="Album name.")
    cleaned_name = models.CharField(max_length=255, editable=False, blank=True, null=True, help_text="Base name without any punctuation or anything weird.")
    slug = models.SlugField('slug', max_length=255, blank=True, help_text='Will be produced from name.')
    image = models.ImageField('Image',upload_to="albums", blank=True, help_text='An image of the album. This is resized to 150x150px automatically.')
    created = models.DateTimeField(auto_now_add=True, help_text="When this album was created.")
    modified = models.DateTimeField(auto_now=True, help_text="When this album was last modified.")

    is_public = models.BooleanField(default=True, help_text="If marked false this album will not be displayed publicly.")
    is_valid = models.BooleanField(default=False, help_text="False means the album will need to be reviewed before it appears on the site. OR needs credible source.")
    uploader = models.ForeignKey(User, blank=True, null=True, help_text="The user who added this album.")

    last_edit = models.CharField(max_length=255, editable=False, blank=True, null=True, help_text="Last editor of this album.")

    objects = AlbumManager()
    artist = models.ForeignKey(Artist, related_name="albums", help_text="The artist this album belongs to.")
    
    #Album Information
    release_date = models.DateTimeField(blank=True, null=True,  help_text="The date this album was released. ex. 2010-03-09 (yyyy-mm-dd)")
    mbid = models.CharField('MusicbrainzID', blank=True, max_length=255, help_text="The ID of this album on Musicbrainz")
    tags = TagField(blank=False, help_text="Tags seperated by comma.")
    
    #scraper utils
    mbid_tracks = models.BooleanField(default=False, editable=False)
    lastfm_valid = models.BooleanField(default=False, editable=False)

    is_deleted = models.BooleanField(default=False, help_text="Marks an album as deleted meaning it won't appear anywhereon the website, but it is still kept in the database so that certain relations don't freak out.") 

    class Meta:
        ordering = ('name', '-created')
        unique_together = ('artist', 'slug') #album unique per artist
        app_label = "submissions"
    
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('album-detail', (), {'artist': self.artist.slug, 'album': self.slug })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.cleaned_name:
            self.cleaned_name = strip_punc(self.name)
        super(Album, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """On delete we need to make sure we get rid of the Tracked object or else we'll have None objects in our database."""
        if self.links.all():
            for link in self.links.all():
                link.delete()
        try:
            tracked = TrackedAlbum.objects.get(ctype=ContentType.objects.get(name='album'), object_id=self.id)
            tracked.delete()
        except TrackedAlbum.DoesNotExist:
            pass #doesn't exist
        super(Album, self).delete(*args, **kwargs)

class AlbumResource(models.Model):
    """
    A resource supports the album in some way.
    """
    name = models.CharField(max_length=255)
    url = models.URLField('URL')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, null=True, blank=True, help_text="If this resource was added by a User.")
    album = models.ForeignKey(Album, related_name="resources")

    class Meta:
        verbose_name = "Album Resource"
        verbose_name_plural = "Album Resources"
        app_label = "submissions"
        unique_together = ('album', 'url')

    def __unicode__(self):
        return self.url
