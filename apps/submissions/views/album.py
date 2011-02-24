from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from submissions.forms import ReportAlbumForm, AlbumEditForm, AlbumForm, BaseAlbumFormSet, AlbumResourceForm, AddArtworkForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from messaging.models import UserMessage
from django.core.mail import send_mail
from django.contrib import messages
from django.forms.formsets import formset_factory
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link
from tagging.models import Tag, TaggedItem
from reporting.models import Report
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from django.views.decorators.cache import cache_page
from activity.signals import add_object, edit_object, delete_object
from tracking.signals import hit
import inspect

def album_detail(request, artist, album):
    """
    A detailed view of an artist. 
    """
    artist = get_object_or_404(Artist, slug__iexact=artist)
    album_obj = get_object_or_404(Album, artist=artist, slug=album)
    hit.send(sender='album_detail', object=album_obj, request=request)
    return list_detail.object_detail(
        request,
        queryset = Album.objects.all(),
        object_id = album_obj.id,
        template_object_name = "album",
        extra_context = { 'artist': artist },
    )

@login_required
def add_album(request, artist):
    """ 
    A view for adding an album on the website.
    Allows multiple albums via formset.
    """
    artist = Artist.objects.get(slug__iexact=artist)
    AlbumFormSet = formset_factory(AlbumForm, formset=BaseAlbumFormSet)
    if request.method == 'POST':
        formset = AlbumFormSet(request.POST, request.FILES)
        if formset.is_valid():
            cleaned_data = formset.cleaned_data
            for data in cleaned_data:
                try:
                    #for each dict in cleaned_data try to save an Album instance.
                    album = Album(
                        name = data['name'], 
                        image = data['image'],
                        release_date = data['release_date'],
                        tags = data['tags'],
                        artist = artist,
                        uploader = request.user,
                        is_valid = True, #user added so its most likely valid
                    )
                    album.save()
                    add_object.send(sender=inspect.stack()[0][3], instance=album, action="Add")
                except IntegrityError: #duplicate trying to be added
                    messages.error(request, "It seems there was a duplicate album for this tist.")
                    return HttpResponseRedirect(reverse('add-album', args=[artist.slug]))
                except Exception, e:
                    raise e
            messages.success(request, "Album(s) added successfully for %s." % (artist.name,))
            return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))
    else:
        formset = AlbumFormSet()
    return render_to_response('submissions/addalbum.html', {
        'artist': artist,
        'formset': formset,
    }, context_instance=RequestContext(request))

@login_required
def edit_album(request, artist, album):
    """
    A view for editing an album on the website.
    Saves via modelform.
    """
    user = request.user
    artist = Artist.objects.get(slug__iexact=artist)
    album = get_object_or_404(Album, slug__iexact=album, artist=artist)
    if request.method == 'POST': 
        form = AlbumEditForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            a = form.save(commit=False)
            a.last_edit = user.username
            a.save()
            edit_object.send(sender=inspect.stack()[0][3], instance=a, action="Edit")
            messages.success(request, "Your changes for \"%s\" have been saved." % (album.name))
            return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
    else:
        form = AlbumEditForm(instance=album)
    return render_to_response('submissions/editalbum.html', {
        'artist': artist,
        'album': album,
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def report_album(request, artist, album):
    """
    A view for reporting an album on the website.
    View is responsible for creating inbox messages to the target user and sending email.
    """
    artist = Artist.objects.get(slug__iexact=artist)
    album = Album.objects.get(slug__iexact=album, artist=artist)
    if request.method == 'POST':
        form = ReportAlbumForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            reason = cd['reason']
            
            try:
                report = Report( #save new reprot object
                    user = request.user,
                    ctype = ContentType.objects.get_for_model(Album),
                    object_id = album.id,
                    reason = reason,
                )
                report.save()
                
                #send email to uploader with reason
                uploader = album.uploader
                user = request.user
                subject = "An %s you uploaded was reported on tehorng!" % (report.ctype,)
                from_email = "Tehorng Staff <staff@tehorng.com>"
                top = "'%s' has reported '%s' for the following reason:\n\n" % (user, report.object.name)
                message = top + reason
                send_mail(subject, message, from_email, [uploader.email])
      
                reports_on_obj = Report.objects.reports_for_id(ctype=ContentType.objects.get_for_model(Album), id=album.id)
           
                g = Group.objects.get(name="Moderator")
 
                if reports_on_obj.count() >= 1:
                    subject =  "Reported Album requires reviewal."
                    from_email ="Tehorng Staff <staff@tehorng.com>"
                    message = "%s has been reported %s times.\nView on tehorng: http://tehorng.com/artists/%s/%s" % (album, reports_on_obj.count(), album.artist.slug, album.slug )
                    
                    reasons_txt = "\n\nReason(s) for report: "

                    for index,r in enumerate(reports_on_obj):
                        reasons_txt += "\nReason %s: %s" % (index, r.reason)

                    message += reasons_txt 
                    
                    for user in g.user_set.all():
                        send_mail(subject, message, from_email, [user.email])
        
       
            except IntegrityError:
                messages.error(request, "It seems you have already reported that once.")
                return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug])) 
            except Exception, e:
                raise e

            messages.success(request, "Your report was a success. The uploader of this album has been notified.")           
            return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug])) 
    else:
        form = ReportAlbumForm()
    return render_to_response('submissions/reportalbum.html', {
        'artist': artist,
        'album': album,
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def delete_album(request, artist, album, template="tehorng/delete_confirm.html"):
    """
    A view for "deleting" an album from the website. Deleting marks objects is_deleted to True and excludes it from the site.
    """
    artist = Artist.objects.get(slug__iexact=artist)
    album = Album.objects.get(slug__iexact=album, artist=artist)
    
    user = request.user

    if not (user.is_superuser or user.is_staff or user == album.uploader):
        messages.warning(request, "You don't have permission to do that.")
        return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))
    
    if request.method == 'POST' and 'yes' in request.POST:        
        album.is_deleted = True 
        album.save()
        delete_object.send(sender=inspect.stack()[0][3], instance=album, action="Delete")
        messages.success(request, "\"%s\" deleted." % (album.name))
        return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))
    elif request.method == 'POST' and 'no' in request.POST: 
        messages.success(request, "Delete cancelled.")
        return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
    return render_to_response(template, {
        'artist': artist,
        'album': album,
    }, context_instance=RequestContext(request))

@login_required
def addresource_album(request, artist, album):
    artist = get_object_or_404(Artist, slug__iexact=artist)
    album = get_object_or_404(Album, artist=artist, slug__iexact=album)
    user = request.user
    if request.method == 'POST':
        form = AlbumResourceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                resource = form.save(commit=False)
                resource.album = album
                resource.uploader = user
                resource.save()
                messages.success(request, "Album resource added successfully.")
                return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
            except IntegrityError:
                messages.error(request, "An resource with that URL already exists for this album.")
                return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
    else:
        form = AlbumResourceForm()
    return render_to_response('submissions/albumresource.html', {
        'artist': artist,
        'album': album,
        'form': form,
    }, context_instance=RequestContext(request))  

@login_required
def addartwork_album(request, artist, album):
    user = request.user
    artist = get_object_or_404(Artist, slug__iexact=artist)
    album = get_object_or_404(Album, artist=artist, slug__iexact=album)
    if album.image:
        messages.error(request, "Album already has an image!")
        return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
    
    if request.method == 'POST':
        form = AddArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            imagedata = form.files['image']
            album.image = imagedata
            album.save()
            messages.success(request, "Artwork for album added!")
            return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
    else:
        form = AddArtworkForm()
    return render_to_response('submissions/addartwork.html', {
        'artist': artist,
        'album': album,
        'form': form,
    }, context_instance=RequestContext(request))

