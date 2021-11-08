from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('reviews/', include('moviereviews.urls')),
    path('admin/', admin.site.urls),
]
