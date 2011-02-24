from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from submissions.forms import ArtistForm, ArtistEditForm, ReportArtistForm, ArtistResourceForm, AddArtworkForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from messaging.models import UserMessage
from django.core.mail import send_mail
from django.contrib import messages
from tracking.models import TrackedArtist
from django.core.paginator import Paginator, InvalidPage
from django.forms.formsets import formset_factory
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link
from tagging.models import Tag, TaggedItem
from django.core.paginator import Paginator, InvalidPage
from reporting.models import Report
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from activity.signals import add_object, edit_object, delete_object 
from tracking.signals import hit
import inspect

ALPHABET = ['0-9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def artist_list(request, letter=None, filter=None):
    """
    View for displaying artists.
    Returns the artist list, by filter. If no filter is supplied assumes alphabetcally.
    """
    queryset = Artist.objects.filter(is_valid=True)
    
    if letter and letter == '0-9':
            queryset = Artist.objects.filter(name__regex=r'^(0|1|2|3|4|5|6|7|8|9)', is_valid=True)
    elif letter:
            queryset = Artist.objects.filter(name__istartswith=letter, is_valid=True)
    
    if filter == "latest":
        queryset = Artist.objects.order_by('-created').filter(is_valid=True)
        #if cache.has_key('latest'):
        #    queryset = cache.get('latest')
        #else:
        #    generated = cache.set('latest', queryset, 3600) #1hr
        #    queryset = cache.get('latest')
    if filter == "popular":
        queryset = TrackedArtist.objects.order_by('-hits') 
    if filter == "withalbums":
        queryset = Artist.objects.filter(albums__isnull=False, is_valid=True).distinct()
    if filter == "noalbums":
        queryset = Artist.objects.filter(albums__isnull=True, is_valid=True).distinct()
    if filter == "withlinks":
        queryset = Artist.objects.filter(albums__links__isnull=False).distinct()
    if filter == "nolinks":
        queryset = Artist.objects.filter(albums__isnull=False, albums__links__isnull=True).distinct()        

    #TODO: Implement ajax loading of filtered results. 
    #if request.is_ajax():
    #   if request.POST and request.POST['filter']:
    #       filter = request.POST['filter']


    #Need to do custom object_list because 'popular' filter produces a non queryset
    #queryset = queryset._clone() in the original code fails
    page = None
    allow_empty = True
    paginate_by = 75

    paginator = Paginator(queryset, paginate_by, allow_empty_first_page=allow_empty)
    if not page:
        page = request.GET.get('page', 1)

    try:
        page_number = int(page)
    except ValueError:
        if page == 'last':
            page_number = paginator.num_pages
        else:
            # Page is not 'last', nor can it be converted to an int.
            raise Http404

    try:
        page_obj = paginator.page(page_number)
    except InvalidPage:
        raise Http404

    context = RequestContext(request,  {
        'alphabet': ALPHABET,
        'filter': filter,
        'letter': letter,
        'alphabet': ALPHABET,
        'paginator': paginator,
        'artist_list': page_obj.object_list,
        'artist_list_count': queryset.count(),
        'total_artists': Artist.objects.filter(is_valid=True, is_deleted=False).count(),
        'pending_artists': Artist.objects.filter(is_valid=False).count(),
        'total_albums': Album.objects.filter(is_valid=True).count(),
        'pending_albums': Album.objects.filter(is_valid=False).count(),
        'page_obj': page_obj,
        # Legacy template context stuff. New templates should use page_obj
        # to access this instead.
        'is_paginated': page_obj.has_other_pages(),
        'results_per_page': paginator.per_page,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'page': page_obj.number,
        'next': page_obj.next_page_number(),
        'previous': page_obj.previous_page_number(),
        'first_on_page': page_obj.start_index(),
        'last_on_page': page_obj.end_index(),
        'pages': paginator.num_pages,
        'hits': paginator.count,
        'page_range': paginator.page_range,
    })
    return render_to_response('submissions/artist_list.html', context)

def artist_detail(request, artist):
    """
    A detailed view of an artist. 
    """
    artist_obj = get_object_or_404(Artist, slug=artist)
    hit.send(sender='artist_detail', object=artist_obj, request=request)
    return list_detail.object_detail(
        request,
        queryset = Artist.objects.all(),
        slug = artist,
        template_object_name = "artist",
    )

@login_required
def add_artist(request, template='submissions/addartist.html'):
    """
    View for adding new artist to the website.
    """
    user = request.user
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            artist = form.save(commit=False) #modelform requires all fields (we need to prefill excluded)
            artist.uploader = user
            if user.is_staff:
                artist.is_valid = True #because a user is adding we need to review this first
                artist.save()
                add_object.send(sender=inspect.stack()[0][3], instance=artist, action="Add")
                messages.success(request, "Artist added successfully. (Since you are staff)")
                return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))
            else:
                artist.is_valid = False #because a user is adding we need to review this first
                artist.save()
                add_object.send(sender=inspect.stack()[0][3], instance=artist, action="Add")
                messages.success(request, "Thanks! Artist has been queued up for approval. =)")
                return HttpResponseRedirect(reverse('artist-index'))
    else:
        form = ArtistForm()
    return render_to_response(template, {
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def edit_artist(request, artist):
    """
    View for editing an artist on the website.
    Saves via modelform.
    """
    user = request.user
    artist = get_object_or_404(Artist, slug=artist) 
    if request.method == 'POST':
        form = ArtistEditForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            artist = form.save(commit=False)
            artist.last_edit = user.username
            artist.save()
            edit_object.send(sender=inspect.stack()[0][3], instance=artist, action="Edit")
            messages.success(request, "Your changes for \"%s\" have been saved." % (artist.name))
            return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))
    else:
        form = ArtistEditForm(instance=artist)
    return render_to_response('submissions/editartist.html', {
        'artist': artist,
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def report_artist(request, artist):
    """
    View for reporting an artist on the website.
    View should be responsible for creating user PM's and sending email.
    """
    artist = get_object_or_404(Artist, slug=artist)
    if request.method == 'POST':
        form = ReportArtistForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            reason = cd['reason']   
            try:
                report = Report( #save new report object
                    user = request.user,
                    ctype = ContentType.objects.get_for_model(Artist),
                    object_id = artist.id,
                    reason = reason,
                )
                report.save()
                
                #send email to uploader with reason
                uploader = artist.uploader
                user = request.user
                subject = "An %s you uploaded was reported on tehorng!" % (report.ctype,)
                from_email ="Tehorng Staff <staff@tehorng.com>"
                top = "'%s' has reported '%s' for the following reason:\n\n" % (user, report.object.name)
                message = top + reason
                send_mail(subject, message, from_email, [uploader.email])
           
                reports_on_obj = Report.objects.reports_for_id(ctype=ContentType.objects.get_for_model(Artist), id=artist.id)
           
                g = Group.objects.get(name="Moderator")
 
                if reports_on_obj.count() >= 1:
                    subject =  "Reported Artist requires reviewal."
                    from_email ="Tehorng Staff <staff@tehorng.com>"
                    message = "%s has been reported %s times.\nView on tehorng: http://tehorng.com/artists/%s" % (artist, reports_on_obj.count(), artist.slug)
                    reasons_txt = "\n\nReason(s) for report: "
                    
                    for index,r in enumerate(reports_on_obj):
                        reasons_txt += "\nReason %s: %s" % (index, r.reason)

                    message += reasons_txt 
                   
                    for user in g.user_set.all(): 
                        send_mail(subject, message, from_email, [user.email])
        
            except IntegrityError:
                messages.error(request, "It seems you have already reported that once.")
                return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug])) 
            except Exception, e:
                raise e
            
            messages.success(request, "Your report was a success. The uploader of this artist has been notified.")          
            return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug])) 
    else:
        form = ReportArtistForm()
    return render_to_response('submissions/reportartist.html', {
        'artist': artist,
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def delete_artist(request, artist, template="tehorng/delete_confirm.html"):
    """
    View for "deleteing" an artist on the website. Deleting marks objects is_deleted to True and excludes it from the site.
    """
    artist = Artist.objects.get(slug__iexact=artist)
    
    user = request.user

    if not (user.is_superuser or user.is_staff or user == artist.uploader):
        messages.warning(request, "You don't have permission to do that.")
        return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))

    if request.method == 'POST' and 'yes' in request.POST:        
        artist.is_deleted = True 
        artist.save()
        delete_object.send(sender=inspect.stack()[0][3], instance=artist, action="Delete")
        messages.success(request, "\"%s\" deleted." % (artist.name,))
        return HttpResponseRedirect(reverse('artist-index'))
    elif request.method == 'POST' and 'no' in request.POST: 
        messages.success(request, "Delete cancelled.")
        return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))
    return render_to_response(template, {'artist': artist}, context_instance=RequestContext(request))

@login_required
def addresource_artist(request, artist):
    user = request.user
    artist = get_object_or_404(Artist, slug__iexact=artist)
    
    if request.method == 'POST':
        form = ArtistResourceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                resource = form.save(commit=False)
                resource.artist = artist
                resource.uploader = user
                resource.save()
                messages.success(request, "Artist resource added successfully.")
                return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))
            except IntegrityError: #dupe resource
                messages.error(request, "An resource with that URL already exists for this artist! =(")
                return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))
    else:
        form = ArtistResourceForm()
    
    return render_to_response('submissions/artistresource.html', {
        'artist': artist,
        'form': form,
    }, context_instance=RequestContext(request))


@login_required
def addartwork_artist(request, artist):
    user = request.user
    artist = get_object_or_404(Artist, slug__iexact=artist)
    
    if artist.image:
        messages.error(request, "Artist already has an image!")
        return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))
    
    if request.method == 'POST':
        form = AddArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            imagedata = form.files['image']
            artist.image = imagedata
            artist.save()
            messages.success(request, "Artwork for artist added!")
            return HttpResponseRedirect(reverse('artist-detail', args=[artist.slug]))
    else:
        form = AddArtworkForm()
    return render_to_response('submissions/addartwork.html', {
        'artist': artist,
        'form': form,
    }, context_instance=RequestContext(request))

