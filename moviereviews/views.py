from .utils import get_movie_reviews
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic, View

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import BookmarkFolder, Bookmark
class IndexView(View):
  template_name = 'moviereviews/index.html'

  def get(self, request, *args, **kwargs):
    params = request.GET
    offset = int(params.get('offset', 0))
    query = params.get('query', 0)
    context = {}

    try:
      has_prev, results, has_next = get_movie_reviews(query, offset)

      if request.user.is_authenticated:
        user = self.request.user
        for review in results:
          bookmark = Bookmark.objects.filter(
            folder__owner=user, link=review['link']['url']).only('id')
          if bookmark.exists():
            review['bookmark_id'] = bookmark.first().id

        context['folders'] = BookmarkFolder.objects.filter(owner=user)

      context['has_prev'] = has_prev
      context['has_next'] = has_next
      context['results'] = results
    except Exception as e:
      context["error_message"] = e

    return render(request, self.template_name, context)

  def post(self, request, *args, **kwargs):
    action = self.request.POST.get('action')

    if action == 'create-folder':
        name = request.POST.get('name', '')
        if len(name) == 0:
          return JsonResponse({
            'success': False,
            'error_message': 'Folder name must not be empty'
          })

        folder = BookmarkFolder.objects.create(name=name, owner=self.request.user)
        return JsonResponse({
          'success': True,
          'data': {
            'name': folder.name,
            'id': folder.id
          }
        })
    elif action == 'create-bookmark':
      payload = request.POST
      name = payload.get('name', '')
      folder_id = payload.get('folder_id', -1)
      url = payload.get('url', '')

      if len(name) == 0:
          return JsonResponse({
            'success': False,
            'error_message': 'Bookmark name must not be empty'
          })
      try:
        folder = BookmarkFolder.objects.get(pk=folder_id)
        bookmark = Bookmark.objects.create(name=name, link=url, folder=folder)
        return JsonResponse({
            'success': True,
            'data': {
              'name': bookmark.name,
              'id': bookmark.id
            }
        })
      except BookmarkFolder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error_message': 'Invalid bookmarks folder'
        })

    elif action == 'delete-bookmark':
      bookmark_id = request.POST.get('bookmark_id', -1)
      try:
        Bookmark.objects.filter(pk=bookmark_id).delete()
        return JsonResponse({
            'success': True,
        })
      except Bookmark.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error_message': 'Bookmark does not exist'
        })

class BookmarksView(LoginRequiredMixin, TemplateView):
  template_name = 'moviereviews/bookmarks.html'
  login_url = '/admin/login/'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['folders'] = BookmarkFolder.objects.filter(
      owner=self.request.user, bookmarks__isnull=False).distinct().order_by(
        'name')
    return context
