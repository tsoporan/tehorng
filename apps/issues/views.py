from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse

from issues.forms import IssueForm, IssueEditForm
from issues.models import Issue

from django.contrib import messages

def issues_list(request, template='issues/issue_list.html'):
    issues = Issue.objects.all()
    return render_to_response(template, {
        'issues': issues,
    }, context_instance=RequestContext(request))

@login_required
def create_issue(request, template='issues/create_issue.html'):
    if request.method == 'POST' and request.POST:
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.submitter = request.user
            issue.save()
            messages.success(request, u"Issue created, pending approval.")
            return HttpResponseRedirect(reverse('issue-detail', args=[issue.id] ))           
    else:
        form = IssueForm()
    return render_to_response(template, {
        'form': form,
    }, context_instance=RequestContext(request)) 

def issue_detail(request, issue_id, template='issues/issue_detail.html'):
    issue = get_object_or_404(Issue, pk=issue_id)

    context = {'issue': issue}

    if request.user.is_staff():
        if request.method == 'POST' and request.POST:
            form = IssueEditForm(request.POST, instance=issue)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('issue-detail', args=[issue.id]))
        else:
            form = IssueEditForm(instance=issue)

        context['form'] = form

    return render_to_response(template, context, context_instance=RequestContext(request))
