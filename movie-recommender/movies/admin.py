from django.contrib import admin
from movies.models import Movie, Genre
from movies.forms import MovieChangeListForm

# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)