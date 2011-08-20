from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from submissions.forms import LinkForm, ReportLinkForm, LinkEditForm, BaseLinkFormSet
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
from submissions.models.utils import gen_hash
from django.db.utils import IntegrityError
from reporting.models import Report
from django.contrib.contenttypes.models import ContentType
from activity.signals import add_object, edit_object, delete_object
import inspect

@login_required
def add_link(request, artist, album):
    """
    View for adding an link to the website.
    Allows multiple links to be added via formset.
    """
    artist = Artist.objects.get(slug__iexact=artist)
    album = Album.objects.get(slug__iexact=album, artist=artist)
    LinkFormSet = formset_factory(LinkForm, formset=BaseLinkFormSet)
    if request.method == 'POST':
        formset = LinkFormSet(request.POST)
        if formset.is_valid():
            cleaned_data = formset.cleaned_data
            for data in cleaned_data:
                try:
                    #for every data dict try to save an Link
                    link = Link(
                        url = data['url'],
                        url_type = data['url_type'],
                        bitrate = data['bitrate'],
                        format = data['format'],
                        album = album,
                        hash = gen_hash(data['url']),
                        uploader = request.user,
                    ) 
                    link.save()
                    add_object.send(sender=inspect.stack()[0][3], instance=link, action="Add")
                except IntegrityError:
                    messages.error(request, "It seems there was a duplicate link for this album.")
                    return HttpResponseRedirect(reverse('add-link', args=[artist.slug, album.slug]))
            messages.success(request, "Links added successfully for \"%s\"!" % (album.name,))
            return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
    else:
        formset = LinkFormSet()
    return render_to_response('submissions/addlink.html', {
        'artist': artist,
        'album': album,
        'formset': formset,
    }, context_instance=RequestContext(request))

@login_required
def edit_link(request, artist, album, link):
    """
    View for editing an link on the website.
    Saves via modelform.
    """
    user = request.user
    artist = Artist.objects.get(slug__iexact=artist)
    album = Album.objects.get(slug__iexact=album, artist=artist)
    link = Link.objects.get(id=link, album=album)
    if request.method == 'POST':
        form = LinkEditForm(request.POST, instance=link)
        if form.is_valid():
            l = form.save(commit=False)
            l.last_edit = user.username
            l.save()
            edit_object.send(sender=inspect.stack()[0][3], instance=l, action="Edit")
            messages.success(request, "Your changes for \"%s\"'s link have been saved." % (album.name))
            return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
    else:
        form = LinkEditForm(instance=link)
    return render_to_response('submissions/editlink.html', {
        'artist': artist,
        'album': album,
        'link': link,
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def report_link(request, artist, album, link):
    """
    View for reporting a link on the website.
    """
    artist = Artist.objects.get(slug__iexact=artist)
    album = Album.objects.get(slug__iexact=album, artist=artist)
    link = Link.objects.get(id=link, album=album)
    if request.method == 'POST':
        form = ReportLinkForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            reason = cd['reason']

            try:
               report = Report( #save new report object
                   user = request.user,
                   ctype = ContentType.objects.get_for_model(Link),
                   object_id = link.id,
                   reason = reason,
               )
               report.save()
                          
               #send email to uploader with reason
               uploader = link.uploader
               user = request.user
               subject = "An %s you uploaded was reported on tehorng!" % (report.ctype,)
               from_email = "Tehorng Staff <staff@tehorng.com>"
               top = "'%s' has reported '%s' for the following reason:\n\n" % (user, report.content_object.url)
               message = top + reason
               send_mail(subject, message, from_email, [uploader.email])
               
               reports_on_obj = Report.objects.reports_for_id(ctype=ContentType.objects.get_for_model(Link), id=link.id)
           
               g = Group.objects.get(name="Moderator")
 
               if reports_on_obj.count() >= 1:
                   subject =  "Reported Link requires reviewal."
                   from_email ="Tehorng Staff <staff@tehorng.com>"
                   message = "%s has been reported %s times.\nView on tehorng: http://tehorng.com/artists/%s/%s" % (link, reports_on_obj.count(), link.album.artist.slug, link.album.slug)
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
            
            messages.success(request, "Your report was a success. The uploader of this link has been notified.")
            return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
    else:
        form = ReportLinkForm()
    return render_to_response('submissions/reportlink.html', {
        'artist': artist,
        'album': album,
        'link': link, 
        'form': form,
    }, context_instance=RequestContext(request))

@login_required 
def delete_link(request, artist, album, link, template='tehorng/delete_confirm.html'):
    """
    A view for "deleting" a link from the website. Deleting marks objects is_deleted to True and excludes it from the site.
    """
    artist = Artist.objects.get(slug__iexact=artist)
    album = Album.objects.get(slug__iexact=album, artist=artist)
    link = Link.objects.get(id__iexact=link, album=album)
    
    user = request.user

    if not (user.is_superuser or user.is_staff or user == link.uploader):
        return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))

    if request.method == 'POST' and 'yes' in request.POST:
        link.is_deleted = True
        link.save()
        delete_object.send(sender=inspect.stack()[0][3], instance=link, action="Delete")
        messages.success(request, "\"%s\" deleted." % link)
        return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))
    elif request.method == 'POST' and 'no' in request.POST:
        messages.success(request, "Delete cancelled.")
        return HttpResponseRedirect(reverse('album-detail', args=[artist.slug, album.slug]))

    return render_to_response(template, {
        'artist': artist,
        'album': album,
        'link': link,
    }, context_instance=RequestContext(request))




