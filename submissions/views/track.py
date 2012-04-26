from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from messaging.models import UserMessage
from django.core.mail import send_mail
from django.contrib import messages
from django.forms.formsets import formset_factory
from submissions.forms import TrackForm, BaseTrackFormSet
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link
from submissions.models.track import Track
from submissions.models.utils import gen_hash
from django.db.utils import IntegrityError
from reporting.models import Report
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelformset_factory
from django.forms.models import model_to_dict
from django.forms.models import inlineformset_factory
from activity.signals import add_object, edit_object, delete_object
import inspect

@login_required
def add_tracks(request, artist, album):
    artist = get_object_or_404(Artist, slug__iexact=artist)
    album = get_object_or_404(Album, slug__iexact=album, artist=artist)

    if album.tracks.all():
        #has tracks we redirect to edit
        return HttpResponseRedirect(reverse('edit-tracks', args=[artist.slug, album.slug]))

    TrackFormSet = formset_factory(TrackForm, formset=BaseTrackFormSet, extra=5)
    if request.method == 'POST':
        formset = TrackFormSet(request.POST)
        if formset.is_valid():
            cleaned_data = formset.cleaned_data
            for data in cleaned_data:
                track = Track()
                track.track_number = data['track_number'] 
                track.title = data['title']
                track.duration = data['duration']
                track.uploader = request.user
                track.album = album
                track.save()
                add_object.send(sender=inspect.stack()[0][3], instance=track, action="Add")
                messages.success(request, "Tracks added for %(album)s" % {'album': album})
                return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
    else:
        formset = TrackFormSet()
    return render_to_response('submissions/addtracks.html', {
        'artist': artist,
        'album': album,
        'formset': formset,
    }, context_instance=RequestContext(request))

@login_required
def manage_tracks(request, artist, album):
    artist = get_object_or_404(Artist, slug__iexact=artist)
    album = get_object_or_404(Album, slug__iexact=album, artist=artist)

    #TrackFormSet = formset_factory(TrackForm, formset=BaseTrackFormSet,can_delete=True, extra=3)

    #tracks = Track.objects.filter(album=album)

    TrackInlineFormSet = inlineformset_factory(Album, Track, fields=('track_number', 'title', 'duration'))    

    if request.method == 'POST':
        #formset = TrackFormSet(request.POST)
        
        formset = TrackInlineFormSet(request.POST, instance=album)
        if formset.is_valid():
            #cleaned_data = formset.cleaned_data
            #deleted_data = formset.deleted_forms
            #for data in cleaned_data:
            #    track = Track.objects.get(id=data['id'])
            #    track.title = data['title'] or "None"
            #    track.track_number = data['track_number'] or None
            #    track.duration = data['duration'] or 0
            #    track.save()
            if 'continue' in request.POST:
                formset.save()
                messages.success(request, "Changes saved! Feel free to add more.")
                return HttpResponseRedirect(reverse('manage-tracks', args=[artist.slug, album.slug]))
            formset.save()
            messages.success(request, "Changes saved!")
            return HttpResponseRedirect(reverse("album-detail", args=[artist.slug, album.slug]))
    else:
        #initial_data = [model_to_dict(track, fields=('id', 'track_number', 'title', 'duration')) for track in tracks]
        #formset = TrackFormSet(initial=initial_data)
        formset = TrackInlineFormSet(instance=album)    

    return render_to_response('submissions/edittracks.html', {
        'artist': artist,
        'album': album,
        'formset': formset,
    }, context_instance=RequestContext(request))
            

