# Movie Recommendation System

Ever since I started learning Artificial Intelligence, I wanted to build projects that have real-world applications. So, when I began with supervised learning, I was very curious to know what the dataset for a movie recommendation system would be. That curiosity prompted me to build a prototype of a Movie Recommendation System, the system is built using Django, integrated with serialized trained models, and draws UI inspiration from Amazon Prime Video.

Dataset: https://www.kaggle.com/datasets/shubhammehta21/movie-lens-small-latest-dataset

## How do recommendation systems work?
When building recommendation systems, there are two different approaches:
- Content-Based Filtering  
- Collaborative Filtering

### Content-Based Filtering
Content-based recommendations are provided based on the similarity between the items. For example, in the context of a movie recommendation system, if User-A watches Movie-A, then movies of the same type or movies related to Movie-A will be recommended to User-A.

### Collaborative Filtering
Collaborative filtering is a recommendation strategy that considers the user’s behavior and compares it with other users in the database. It doesn’t solely depend on one user’s data for modeling. There are various approaches to implement collaborative filtering, but the key concept is the collective influence of multiple users on the recommendation outcome.

![image](https://github.com/abdulhakkeempa/movie-recommender/assets/92361680/bd0249af-d6e5-4535-a95a-d3aee7aa8a09)
*Representation of Content-Based Filtering & Collaborative Filtering*

<strong>In this project, I have implemented `Item-Item Collaborative Filtering + Content-Based Filtering`.</strong>

### Item-Item Collaborative Filtering
For example, when comparing movies 'A' and 'B', we analyze the ratings given by users who rated both movies. If these ratings show high similarity, it indicates that 'A' and 'B' are similar movies. Thus, if someone liked 'A', they should be recommended 'B', and vice versa.

This approach will help us solve the cold start problem when a new user comes in. Also, Content-Based Filtering is provided in parallel to recommend movies on a similar basis by analyzing the cosine similarity.

### Screenshots

![image](https://github.com/abdulhakkeempa/movie-recommender/assets/92361680/79204d2d-7226-433c-a73c-a5c65e77d727)
![image](https://github.com/abdulhakkeempa/movie-recommender/assets/92361680/cafb99e6-dd0d-4f6f-99dd-c2cedfe369cc)
![image](https://github.com/abdulhakkeempa/movie-recommender/assets/92361680/e2a13d33-6fa0-49e1-b0c2-f5c46b7f7d43)
![image](https://github.com/abdulhakkeempa/movie-recommender/assets/92361680/442ea2e8-c432-4212-885b-5e7b754c8b99)

### How to Install and Run the Project
1. `git clone https://github.com/abdulhakkeempa/movie-recommender.git`
2. `cd movie-recommender`
3. Create a venv and activate it.
    * Linux / MacOS
    ```
    python3 -m venv venv
    ./venv/bin/activate
    ```
    * Windows
    ```
    python3 -m venv venv
    venv\Scripts\activate
    ```
4. `pip install -r requirements.txt`
5. Copy .env.example as .env and fill in the values.
6. Run this command to load movies which are in the dataset from TMDB.  
   `python manage.py load_movies` 
7. `python manage.py runserver`
8.  Create an account and use the platform.  
    Go to `http://localhost:8000/register`

#### If you want to access the admin panel and add movies from the admin panel
1. `python manage.py createsuperuser`
2. `python manage.py runserver`
3. Login with the newly created admin credentials.  
   Go to `http://localhost:8000/admin`

## References
1. https://www.analyticsvidhya.com/blog/2020/11/create-your-own-movie-movie-recommendation-system/#h-removing-noise-from-the-data
2. https://towardsdatascience.com/hands-on-content-based-recommender-system-using-python-1d643bf314e4
3. https://ieee-dataport.org/open-access/imdb-users-ratings-dataset
4. https://datajobs.com/data-science-repo/Recommender-Systems-[Netflix].pdf

## License
This project is licensed under the terms of the GNU General Public License. If you encounter any issues or have suggestions for improvements, please add them to the project's issue tracker. Your contributions are greatly appreciated!
