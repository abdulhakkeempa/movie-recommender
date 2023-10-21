from django.shortcuts import render
from django.views import View

# Create your views here.
class Movies(View):
  def get(self, request):
    return render(request, 'movies/movies.html')