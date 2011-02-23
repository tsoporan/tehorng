from django.db import models
from submissions.models.utils import gen_hash, strip_punc, get_artist_path
from django.template.defaultfilters import slugify
from submissions.managers import ArtistManager
from django.contrib.auth.models import User
from tagging.fields import TagField
from tracking.models import TrackedArtist
from django.contrib.contenttypes.models import ContentType

class Artist(models.Model):
    """
    A single unique artist.
    """
    name = models.CharField(max_length=255, unique=True, help_text="Artist name must be unique.")
    cleaned_name = models.CharField(max_length=255, blank=True, null=True, editable=False, help_text="Base name without any punctuation or anything weird.")
    slug = models.SlugField(unique=True, max_length=255, blank=True, help_text="Slugs are auto-determined from name on save. The slug field will also be the URL.")
    image = models.ImageField(upload_to="artists", blank=True, help_text="An image of the artist. This is turned into a 250x250 thumbnail.")

    created = models.DateTimeField(auto_now_add=True, help_text="When this artist was created.")
    modified = models.DateTimeField(auto_now=True, help_text="When this artist was last modified.")

    is_dmca = models.BooleanField(default=False, help_text="If an DMCA request has been sent for this artist, mark this False and their links will not be displayed.")
    is_valid = models.BooleanField(default=False, help_text="False meaning they will need to be reviewed before appearing on the site. Or needs credible source.")
    is_public = models.BooleanField(default=True, help_text="If this is set to false the artist will not be displayed on the site live.")
    is_verified = models.BooleanField(default=False, help_text="This is true when an artist gets in touch with us about their tehorng page and would like to be given rights to change the page as they see fit. In cases like these the artist will have complete control over the presentation of the page and the material in it and users will not be able to edit any information.")

    objects = ArtistManager()

    uploader = models.ForeignKey(User, blank=True, null=True, help_text="The user who added thist artist.")
    
    last_edit = models.CharField(max_length=255, editable=False, blank=True, null=True, help_text="Last editor of this artist.")

    #Artist Information
    #formed = models.DateTimeField(blank=True, null=True, help_text="When this artist formed. In the format yyyy-mm-dd")
    formed = models.IntegerField(max_length=4, blank=True, null=True, help_text="When this artist formed. Must be a 4 digit number, representing the year. ex. 2010")
    origin = models.CharField(blank=True, max_length=255, help_text="Artists origin. ex. San Diego, California, United States")
    members = models.CharField(blank=True, max_length=255, help_text="Members in the band.")
    biography = models.TextField(blank=True, help_text="Artist biography.")
    is_touring = models.BooleanField(default=False, help_text="Is this artist on tour?")
    mbid = models.CharField('MusicbrainzID', blank=True, max_length=255, help_text="The ID of this artist on Musicbrainz")
    tags = TagField(help_text="Tags seperated by comma. Example: gospel, praise, worship", blank=False)

    #scraper stuff
    mbid_tracks = models.BooleanField(editable=False, default=False)
    lastfm_valid = models.BooleanField(editable=False, default=False)
    
    is_deleted = models.BooleanField(default=False, help_text="Marks an Artist as deleted meaning it won't appear anywhere on the website, but it is still kept in the database so that certain relations don't freak out.")

    class Meta:
        ordering = ('name',)
        verbose_name = "Artist"
        verbose_name_plural = "Artists"
        app_label = "submissions"

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('artist-detail', (), {'artist': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.cleaned_name:
            self.cleaned_name = strip_punc(self.name).lower().strip()
        
        if self.is_deleted:
            self.name = self.name + u" (Deleted)"
        super(Artist, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """On delete we need to make sure we get rid of the Tracked object or else we'll have None objects in our database."""
        if self.albums.all():
            for album in self.albums.all():
                album.delete()
        try:
            tracked = TrackedArtist.objects.get(ctype=ContentType.objects.get(name='artist'), object_id=self.id)
            tracked.delete()
        except TrackedArtist.DoesNotExist:
            pass #doesn't exist skip
        super(Artist, self).delete(*args, **kwargs)


class ArtistResource(models.Model):
    """
    A resource supports the artist in some way.
    """
    name = models.CharField(max_length=250)
    url = models.URLField('URL')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, null=True, blank=True, help_text="If this resource was added by a User.")
    artist = models.ForeignKey(Artist, related_name='resources')

    class Meta:
        verbose_name = "Artist Resource"
        verbose_name_plural = "Artist Resources"
        app_label = "submissions"
        unique_together = ('artist', 'url')

    def __unicode__(self):
        return self.url
