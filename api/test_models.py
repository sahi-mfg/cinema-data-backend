#%%
from database import SessionLocal
from models import Movie, Rating, Tag, Link
from database import Base

db = SessionLocal()
#%%
# Test de la recupération de quelques films
movies = db.query(Movie).limit(10).all()
for movie in movies:
    print(f"Movie ID: {movie.movieId}, Title: {movie.title}, Genres: {movie.genres}")
# %%
ratings = db.query(Rating).limit(10).all()
for rating in ratings:
    print(f"User ID: {rating.userId}, Movie ID: {rating.movieId}, Rating: {rating.rating}, Timestamp: {rating.timestamp}")
# %%
tags = db.query(Tag).limit(10).all()
for tag in tags:
    print(f"User ID: {tag.userId}, Movie ID: {tag.movieId}, Tag: {tag.tag}, Timestamp: {tag.timestamp}")

# %%
links = db.query(Link).limit(10).all()
for link in links:
    print(f"Movie ID: {link.movieId}, IMDB ID: {link.imdbId}, TMDB ID: {link.tmdbId}")
# %%r
# recupération des films d'actions
action_movies = db.query(Movie).filter(Movie.genres.contains("Action")).limit(10).all()
for movie in action_movies:
    print(f"Movie ID: {movie.movieId}, Title: {movie.title}, Genres: {movie.genres}")
# %%
