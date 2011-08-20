from reporting.models import Report
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError

ctype_for_model = ContentType.objects.get_for_model

@login_required
def report_object(request, ctype, object_id):
    
    ctype = get_object_or_404(ContentType, name__iexact=ctype)    
   
    cobj = get_object_or_404(ctype.model_class(), id=object_id)

    if request.method == 'POST':
        form = ReportObjectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            reason = cd['reason']   
            try:
                report = Report.objects.create(user=request.user, ctype=ctype, object_id=cobj.id, reason=reason)
                report.notify(user=user, object=cobj)
        
            except IntegrityError:
                messages.error(request, "It seems you have already reported that once.")
                return HttpResponseRedirect(cobj.get_absolute_url()) 
            except Exception, e:
                raise e
            
            messages.success(request, "Your report was a success. User has been notified.")          
            return HttpResponseRedirect(cobj.get_absolute_url()) 
    else:
        form = ReportObjectForm(request.POST)
    return render_to_response('submissions/reportobject.html', {
        'object': cobj,
        'type': ctype,
        'form': form,
    }, context_instance=RequestContext(request))


