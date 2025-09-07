"""SQLAlchemy query helper functions for my API."""

from models import Link, Movie, Rating, Tag
from sqlalchemy import func
from sqlalchemy.orm import Session


# --- Films ---
def get_movie(db: Session, movie_id: int):
    """Get a movie by its ID."""
    return db.query(Movie).filter(Movie.movieId == movie_id).first()


def get_movies(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    title: str | None = None,
    genre: str | None = None,
):
    """Get a list of movies with optional filters."""
    query = db.query(Movie)

    if title:
        query = query.filter(Movie.title.ilike(f"%{title}%"))
    if genre:
        query = query.filter(Movie.genres.ilike(f"%{genre}%"))
    return query.offset(skip).limit(limit).all()


# --- Ratings ---
def get_rating(db: Session, user_id: int, movie_id: int):
    """Get a rating by user ID and movie ID."""
    return (
        db.query(Rating)
        .filter(Rating.userId == user_id, Rating.movieId == movie_id)
        .first()
    )


def get_ratings(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    movie_id: int | None = None,
    user_id: int | None = None,
    min_rating: float | None = None,
):
    """Get a list of ratings with optional filters."""
    query = db.query(Rating)

    if movie_id:
        query = query.filter(Rating.movieId == movie_id)
    if user_id:
        query = query.filter(Rating.userId == user_id)
    if min_rating:
        query = query.filter(Rating.rating >= min_rating)
    return query.offset(skip).limit(limit).all()


# --- Tags ---
def get_tag(db: Session, user_id: int, movie_id: int, tag_text: str):
    """Get a tag by user ID, movie ID, and tag text."""
    return (
        db.query(Tag)
        .filter(Tag.userId == user_id, Tag.movieId == movie_id, Tag.tag == tag_text)
        .first()
    )


def get_tags(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    movie_id: int | None = None,
    user_id: int | None = None,
):
    """Get a list of tags with optional filters."""
    query = db.query(Tag)

    if movie_id is not None:
        query = query.filter(Tag.movieId == movie_id)
    if user_id is not None:
        query = query.filter(Tag.userId == user_id)
    return query.offset(skip).limit(limit).all()


# --- Links ---
def get_link(db: Session, movie_id: int):
    """Get a link by movie ID."""
    return db.query(Link).filter(Link.movieId == movie_id).first()


def get_links(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of links with optional filters."""
    return db.query(Link).offset(skip).limit(limit).all()


def get_movie_count(db: Session):
    """Get the total number of movies."""
    return db.query(Movie).count()


def get_rating_count(db: Session):
    """Get the total number of ratings."""
    return db.query(Rating).count()


def get_tag_count(db: Session):
    """Get the total number of tags."""
    return db.query(Tag).count()


def get_link_count(db: Session):
    """Get the total number of links."""
    return db.query(Link).count()


def get_average_rating(db: Session):
    """Get the average rating across all ratings."""
    total_ratings = db.query(Rating).count()
    if total_ratings == 0:
        return 0.0
    total_score = db.query(func.sum(Rating.rating)).scalar() or 0.0
    return total_score / total_ratings
