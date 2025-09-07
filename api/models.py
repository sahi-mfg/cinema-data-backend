"""SQLAlchemy models."""

from database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Movie(Base):
    __tablename__ = "movies"
    movieId = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genres = Column(String)

    # Relationships
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete")
    tags = relationship("Tag", back_populates="movie", cascade="all, delete")
    links = relationship(
        "Link", back_populates="movie", cascade="all, delete", uselist=False
    )


class Rating(Base):
    __tablename__ = "ratings"
    userId = Column(Integer, primary_key=True, index=True)
    movieId = Column(Integer, ForeignKey("movies.movieId"), primary_key=True)
    rating = Column(Float)
    timestamp = Column(Integer)

    # Relationships
    movie = relationship("Movie", back_populates="ratings")


class Tag(Base):
    __tablename__ = "tags"
    userId = Column(Integer, primary_key=True, index=True)
    movieId = Column(Integer, ForeignKey("movies.movieId"), primary_key=True)
    tag = Column(String, primary_key=True)
    timestamp = Column(Integer)

    # Relationships
    movie = relationship("Movie", back_populates="tags")


class Link(Base):
    __tablename__ = "links"
    movieId = Column(Integer, ForeignKey("movies.movieId"), primary_key=True)
    imdbId = Column(String)
    tmdbId = Column(Integer)

    # Relationships
    movie = relationship("Movie", back_populates="links", uselist=False)
