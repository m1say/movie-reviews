from django.shortcuts import render
from .utils import get_movie_reviews
from django.http import HttpResponse
from django.views import generic, View

from django.views.generic.base import TemplateView

class IndexView(View):
  template_name = 'moviereviews/index.html'

  def get(self, request, *args, **kwargs):
    params = request.GET
    offset = int(params.get('offset', 0))
    query = params.get('query', 0)
    context = {}

    try:
      has_prev, results, has_next = get_movie_reviews(query, offset)
      context['has_prev'] = has_prev
      context['has_next'] = has_next
      context['results'] = results
    except Exception as e:
      context["error_message"] = e

    return render(request, self.template_name, context)