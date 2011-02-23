from haystack.views import SearchView
from haystack.forms import SearchForm
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.track import Track


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)

class OrngSearchView(SearchView):
    def __name__(self):
        return "OrngSearchView"

    def build_page(self):
        """
        Returns tehorng specific results in a paginated fashion.
        """
        results = self.results
        return results

    def create_response(self):
        """
        Creates tehorng specific response to send back to user.
        """
        results = self.build_page()
        
        context = {
            'query': self.query,
            'form': self.form,
        }
        if results:
            context.update({
                'artists': results.models(Artist)[:10],
                'albums': results.models(Album)[:10],
                'tracks': results.models(Track)[:20],
            })
        else:
            context.update({
                'noresults': True,
            })
        context.update(self.extra_context()) #if extra context
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))
