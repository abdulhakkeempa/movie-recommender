from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from movies.models import Movie, UserMovieRating
from django.contrib.auth.mixins import LoginRequiredMixin


class ListMovies(LoginRequiredMixin, ListView):
  model = Movie
  context_object_name = 'movies'
  template_name = 'movies/movies.html'

class MovieDetail(LoginRequiredMixin, View):
  def get(self, request, pk):
    movie = Movie.objects.get(pk=pk)
    return render(request, 'movies/movies-individual.html', {'movie': movie})
  
  def post(self, request, pk):
    movie = Movie.objects.get(pk=pk)
    user = request.user
    rating = request.POST.get('review')

    if UserMovieRating.objects.filter(user=user, movie=movie).exists():
      rating = UserMovieRating.objects.get(user=user, movie=movie)
      rating.rating = rating
      rating.save()
      return redirect('movies-individual', pk=pk)

    rating = UserMovieRating(user=user, movie=movie, rating=rating)
    rating.save()
    return redirect('movies-individual', pk=pk)
