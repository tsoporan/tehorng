from django import forms
from django.forms import ModelForm
from django.template.defaultfilters import slugify
import re
import string
from django.forms.formsets import BaseFormSet
from submissions.models.artist import Artist, ArtistResource
from submissions.models.album import Album, AlbumResource
from submissions.models.link import Link
from submissions.models.track import Track
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets

PUNC = string.punctuation

class BaseAlbumFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return 
        names = []
        if not self.forms[0].has_changed(): #if nothing's changed
            raise forms.ValidationError("Hmm, it seems nothing's changed, one form needs to be complete before a save!")
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            #TODO: add datepicker unique class
            name = form.cleaned_data['name']
            if name in names:
                raise forms.ValidationError("There can be no duplicate album names!")
            names.append(name)

class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return 
        urls = []
        if not self.forms[0].has_changed(): #if nothing's changed
            raise forms.ValidationError("Hmm, it seems nothing's changed, one form needs to be complete before a save!")
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            url = form.cleaned_data['url']
            if url in urls:
                raise forms.ValidationError("There can be no duplicate URLs!")
            urls.append(url)

class BaseTrackFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        if not self.forms[0].has_changed():
            raise forms.ValidationError("Hmm, it seems nothing's changed, one form needs to be complete before a save!") 

class TrackForm(ModelForm):
    """
    Form for adding track.
    """
    class Meta:
        model = Track
        fields = ('track_number', 'title', 'duration')

class ArtistForm(ModelForm):
    """
    Form for adding an artist.
    """
    class Meta:
        model = Artist
        fields = ('name', 'image', 'tags')
    
class ArtistEditForm(ModelForm):
    """
    A form for editing the artist based on the Artist model.
    """
    class Meta:
        model = Artist
        exclude = ('slug', 'is_valid', 'is_public','is_dmca', 'is_verified', 'uploader', 'got_tracks')

class AlbumForm(ModelForm):
    """
    Form to add an album.
    """
    #release_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'datepicker'}))
    class Meta:
        model = Album
        exclude = ('cleaned_name', 'slug','artist','created','is_valid', 'url', 'uploader', 'is_public', 'mbid')
    
#    def clean_name(self):
#        super(AlbumForm, self).clean()
#        name = self.cleaned_data['name']
#
#        ALLOWED_PUNC = ['"', "'", ",", "!", "&", "?", ":" ,"-"," "]
#        ALLOWED = string.letters + string.digits + ''.join(ALLOWED_PUNC)
#        
#        flag = 0 
#        for c in name:
#            if c not in ALLOWED:
#                flag = 1
#
#        if flag:
#            raise forms.ValidationError('Album names can only contain letters, numbers, and these symbols: %s' % (''.join(ALLOWED_PUNC),))
#        
#        return name
class AlbumEditForm(ModelForm):
    """
    Form to edit album, only available to the album uploader.
    """
    class Meta:
        model = Album
        exclude = ('cleaned_name', 'slug','artist','created','is_valid', 'url', 'uploader', 'is_public', 'mbid')

class LinkForm(ModelForm): 
    """Form for adding links to the website. """
    class Meta:
        model = Link
        exclude = ('uploader', 'album','created', 'reported', 'hash', 'part', 'expires', 'dead')

    def clean_url(self):
        super(LinkForm, self).clean()
        url = self.cleaned_data['url']
        probablyspam = ['example', 'tehorng', 'porn', 'jizz', 'sex', 'nude', 'gay', 'fag', 'fuck', 'somefile.zip']
        for spam in probablyspam:
            if spam in url:
                raise forms.ValidationError("That doesn't look like a valid URL. If it is please let us know by contacting us.")
        return url

class LinkEditForm(LinkForm):
    """
    Form for editing an link, only available to the link uploader.
    Inherits everything from superclass.
    """
    pass

class ReportArtistForm(forms.Form):
    """
    Form for reporting an artist.
    """
    reason = forms.CharField(max_length=255, required=True, help_text='A brief description of the problem.', widget=forms.Textarea)

class ReportAlbumForm(forms.Form):
    """
    Form for reporting an album.
    """
    reason = forms.CharField(max_length=255, required=True, help_text='A brief description of the problem.', widget=forms.Textarea)

class ReportLinkForm(forms.Form):
    """
    Form for reporting an link.
    """
    reason = forms.CharField(max_length=255, required=True, help_text='A brief description of the problem.', widget=forms.Textarea)

class ArtistResourceForm(ModelForm):
    class Meta:
        model = ArtistResource
        exclude = ('created', 'modified', 'uploader', 'artist')

class AlbumResourceForm(ModelForm):
    class Meta:
        model = AlbumResource
        exclude = ('created', 'modified', 'uploader', 'album')

class AddArtworkForm(forms.Form):
    """Simple generic form for adding an image"""
    image = forms.FileField(help_text="Images are turned into 250x250 thumbnails.")

