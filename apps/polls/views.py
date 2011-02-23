from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages
from django.template import RequestContext
from polls.models import Poll, Choice, Feedback
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from polls.forms import FeedbackForm

#SOLUTION isn't good, but should work for now
IPS = []


def index(request):
    polls = Poll.objects.order_by('-created')
    return render_to_response('polls/index.html', {
        'polls': polls, 
    }, context_instance=RequestContext(request))


def detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    
    cxt = {'poll': poll}
    #semi ugly workaround
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if request.user and request.user.is_authenticated():
                feedback = Feedback.objects.create(poll=poll, user=request.user, body=cd['body'])
            else:
                feedback = Feedback.objects.create(poll=poll, body=cd['body'])
            messages.success(request,"Thanks for the feedback!")
            return HttpResponseRedirect(reverse('poll-detail', args=[poll.id]))
    else:
        form = FeedbackForm()
        cxt.update({'form': form }) 
    return render_to_response('polls/detail.html', cxt, context_instance=RequestContext(request))

def vote(request, poll_id):
    global IPS
    poll = get_object_or_404(Poll, id=poll_id)
    if not poll.type == 'Vote':
        messages.error(request, "You may not vote on this poll.")
        return HttpResponseRedirect(reverse('poll-detail', args=[poll.id])) 

    try:
        choice = poll.choice_set.get(pk=request.POST['choice']) #returns the ID 
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a choice.")
        return HttpResponseRedirect(reverse('poll-detail', args=[poll.id]))
    else:
        if request.META['REMOTE_ADDR'] in IPS:
            messages.error(request, "You may only vote once.")
            return HttpResponseRedirect(reverse('poll-detail', args=[poll.id]))
        choice.votes += 1
        choice.save()
        IPS.append(request.META['REMOTE_ADDR'])
        messages.success(request, "Thank you for voting!")
        return HttpResponseRedirect(reverse('poll-results', args=[poll.id]))

def results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    total = sum([c.votes for c in poll.choice_set.all()])
    return render_to_response('polls/results.html', {
        'poll': poll,
        'total': total,
    }, context_instance=RequestContext(request))
