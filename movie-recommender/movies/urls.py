from django.urls import path, include
from movies.views import Movies, get_movies

urlpatterns = [
    path("", Movies.as_view(), name="movies"),
    path("/<int:pk>", get_movies, name="movies-individual"),
]