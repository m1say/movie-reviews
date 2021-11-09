from django.shortcuts import render
from .utils import get_movie_reviews
from django.http import HttpResponse
from django.views import generic, View

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
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

class BookmarksView(LoginRequiredMixin, TemplateView):
  template_name = 'moviereviews/bookmarks.html'
  login_url = '/admin/login/'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context