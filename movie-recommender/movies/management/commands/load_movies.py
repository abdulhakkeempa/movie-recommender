import csv
import requests
from movies.models import Movie, Genre
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()

TMDB_BEARER_TOKEN = os.getenv('TMDB_API_KEY')
TMDB_API = os.getenv('TMBD_ENDPOINT')
TMDB_IMAGE_URL = os.getenv('TMDB_IMAGE_URL')

class Command(BaseCommand):
    help = 'Loads data from TBDM API and saves it to the database'

    def handle(self, *args, **kwargs):
        print("Loading Movies to DB")

        headers = {
            'Authorization': f'Bearer {TMDB_BEARER_TOKEN}',
        }

        with open('data/links.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                movie_id = row[2]  # Assuming movieId is in the first column

                # Fetch movie data from the API
                request_uri = f'{TMDB_API}/{movie_id}'
                print(request_uri)
                response = requests.get(request_uri, headers=headers)
                data = response.json()
                print(data)

                #extracting year from date.
                print(data['release_date'])
                release_year = datetime.strptime(data['release_date'], "%Y-%m-%d").year

                # Create a new Movie object and save it to the database
                movie = Movie(
                    title=data['original_title'],
                    description=data['overview'],
                    length=int(abs(data['runtime'])),
                    release_year=release_year,
                    language=data['original_language'],
                    poster=f'{TMDB_IMAGE_URL}/{data["backdrop_path"]}',
                )
                
                movie.save()

                for genre in data['genres']:
                    genre_name = genre['name']
                    genre = Genre.objects.filter(name=genre_name)

                    if genre.exists():
                        genre_obj = genre.first()
                    else:
                        genre_obj = Genre.objects.create(name=genre_name)

                    # Add the genre to the movie
                    movie.genres.add(genre_obj)

                movie.save()
                print(f'Saved movie {movie_id} to the database')

        print("Data loaded successfully")
