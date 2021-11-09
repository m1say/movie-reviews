from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'moviereviews'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('bookmarks', views.BookmarksView.as_view(), name='bookmarks'),
]