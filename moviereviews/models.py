from django.db import models
from django.contrib.auth.models import User

class BookmarkFolder(models.Model):
  name = models.CharField(max_length=50)
  owner = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='bookmark_folders')

  def __str__(self):
    return self.name

class Bookmark(models.Model):
  name = models.CharField(max_length=50)
  link = models.CharField(max_length=200)
  folder = models.ForeignKey(
    BookmarkFolder, on_delete=models.CASCADE, related_name='bookmarks')

  def __str__(self):
    return f'{self.name} in {self.folder.name}'