from django.urls import path, include
from movies.views import Movies

urlpatterns = [
    path("", Movies.as_view(), name="movies"),
]