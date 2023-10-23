from django.shortcuts import render
from django.views import View
from movies.models import Movie

# Create your views here.
class Movies(View):
  def get(self, request):
    movies = Movie.objects.all()
    print(movies)
    return render(request, 'movies/movies.html', {'movies': movies})
  

def get_movies(request, pk):
  movie = Movie.objects.get(pk=pk)
  return render(request, 'movies/movies-individual.html', {'movie': movie})