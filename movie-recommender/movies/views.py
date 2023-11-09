from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from movies.models import Movie, UserMovieRating
from django.contrib.auth.mixins import LoginRequiredMixin
from movies.load_models import cosine_sim, movies, csr_data, final_dataset, knn

class ListMovies(LoginRequiredMixin, ListView):
  model = Movie
  context_object_name = 'movies'
  template_name = 'movies/movies.html'

  def get_context_data(self, **kwargs):
      # Call the base implementation first to get a context
      context = super().get_context_data(**kwargs)

      # Get the current user
      user = self.request.user

      context['continue_watching'] = Movie.objects.filter(usermovierating__user=user) #where the users have provided a rating
      # context['recommended'] = Movie.objects.filter(...)  # Replace with your actual query

      return context
  
class MovieDetail(LoginRequiredMixin, View):
  def get(self, request, pk):
    movie = Movie.objects.get(pk=pk)
    rating = int(abs(movie.get_review_values))
    rating_list = [True if i < rating else False for i in range(5)]

    #fetching the rating providied by the user
    try:
      user_rating = UserMovieRating.objects.get(user=request.user, movie=movie)
      user_rating = user_rating.rating
    except UserMovieRating.DoesNotExist:
      user_rating = 0

    return render(request, 'movies/movies-individual.html', {'movie': movie, 'global_rating_list': rating_list, 'user_rating': user_rating})
  
  def post(self, request, pk):
    movie = Movie.objects.get(pk=pk)
    user = request.user
    rating = request.POST.get('review')

    if UserMovieRating.objects.filter(user=user, movie=movie).exists():
      print(rating)
      user_movie_rating  = UserMovieRating.objects.get(user=user, movie=movie)
      user_movie_rating.rating = rating
      user_movie_rating.save()
      return redirect('movies-individual', pk=pk)

    user_movie_rating = UserMovieRating(user=user, movie=movie, rating=rating)
    user_movie_rating .save()
    return redirect('movies-individual', pk=pk)

