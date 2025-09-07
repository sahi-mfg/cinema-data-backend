# %%
from database import SessionLocal
from models import Link, Movie, Rating, Tag

db = SessionLocal()
# %%
# Test de la recupération de quelques films
movies = db.query(Movie).limit(10).all()
for movie in movies:
    print(f"Movie ID: {movie.movieId}, Title: {movie.title}, Genres: {movie.genres}")
# %%
ratings = db.query(Rating).limit(10).all()
for rating in ratings:
    print(
        f"User ID: {rating.userId}, Movie ID: {rating.movieId}, Rating: {rating.rating}, Timestamp: {rating.timestamp}"
    )
# %%
tags = db.query(Tag).limit(10).all()
for tag in tags:
    print(
        f"User ID: {tag.userId}, Movie ID: {tag.movieId}, Tag: {tag.tag}, Timestamp: {tag.timestamp}"
    )

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
high_rated_movies = (
    db.query(Movie.title, Rating.rating)
    .join(Rating)
    .filter(Rating.rating >= 4)
    .limit(5)
    .all()
)
print(f"High Rated Movies (>=4): {high_rated_movies}")
for title, rating in high_rated_movies:
    print(f"Title: {title}, Rating: {rating}")

# %%
# Recupération des tags associés aux films
tags = db.query(Tag).limit(10).all()
for tag in tags:
    print(
        f"User ID: {tag.userId}, Movie ID: {tag.movieId}, Tag: {tag.tag}, Timestamp: {tag.timestamp}"
    )
# %%
# Tester la classe Link
links = db.query(Link).limit(5).all()
for link in links:
    print(f"Movie ID: {link.movieId}, IMDB ID: {link.imdbId}, TMDB ID: {link.tmdbId}")
# %%
# Fermer la session
db.close()
# %%
