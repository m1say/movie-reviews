from django.contrib import admin
from .models import Bookmark, BookmarkFolder

admin.site.register(Bookmark)
admin.site.register(BookmarkFolder)