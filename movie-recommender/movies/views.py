from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from movies.models import Movie, UserMovieRating
from django.contrib.auth.mixins import LoginRequiredMixin
from movies.recommendations import get_item_based_recommendation, get_content_based_recommendations
import re

# Function to remove year from movie title
def remove_year(movie):
    return re.sub(r'\s\(\d{4}\)', '', movie)


class ListMovies(LoginRequiredMixin, ListView):
  model = Movie
  context_object_name = 'movies'
  template_name = 'movies/movies.html'

  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)

    # Get the current user
    user = self.request.user

    context['movies'] = Movie.objects.all()[:50]
    context['continue_watching'] = Movie.objects.filter(usermovierating__user=user) #where the users have provided a rating
    # context['recommended'] = Movie.objects.filter(...)  # Replace with your actual query
    print(self.recommend_movies())
    return context

  def recommend_movies(self, **kwargs):
      movies = self.get_user_watched_movies()
      if movies:
        movie_titles = [movie.title for movie in movies]
        recommended_movies = get_content_based_recommendations(movie_titles)
        print(recommended_movies)
        # Apply function to each movie in the list
        cleaned_data = [remove_year(movie) for movie in recommended_movies[0]] 
        print(cleaned_data)
        recommended_movies = Movie.objects.filter(title__in=cleaned_data)
        return recommended_movies

  def get_user_watched_movies(self, **kwargs):
    """
      Returns the latest 5 movies the user has watched
    """
    user = self.request.user
    return Movie.objects.filter(usermovierating__user=user)[:5]
  
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

