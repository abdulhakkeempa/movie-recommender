from django.urls import path, include
from movies.views import  ListMovies, MovieDetail

urlpatterns = [
    path("", ListMovies.as_view(), name="movies"),
    path("/<int:pk>", MovieDetail.as_view(), name="movies-individual"),
]