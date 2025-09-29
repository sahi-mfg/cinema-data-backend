from pydantic import BaseModel

# --- Schémas secondaires ---


class RatingBase(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    movieId: int
    userId: int
    tag: str
    timestamp: int

    class Config:
        orm_mode = True


class LinkBase(BaseModel):
    imdbId: str | None = None
    tmdbId: int | None = None

    class Config:
        orm_mode = True


# --- Schémas principaux pour Movie ---


class MovieBase(BaseModel):
    movieId: int
    title: str
    genres: str | None = None

    class Config:
        orm_mode = True


class MovieDetailed(MovieBase):
    ratings: list[RatingBase] = []
    tags: list[TagBase] = []
    links: LinkBase | None = None


# --- Schémas pour liste de films (sans détails imbriqués) ---
class MovieSimple(BaseModel):
    movieId: int
    title: str
    genres: str | None = None

    class Config:
        orm_mode = True


# --- Pour les endpoints de /ratings et /tags si appelés seuls ---
class RatingSimple(BaseModel):
    movieId: int
    userId: int
    rating: float
    timestamp: int

    class Config:
        orm_mode = True


class TagSimple(BaseModel):
    movieId: int
    userId: int
    tag: str
    timestamp: int

    class Config:
        orm_mode = True


class LinkSimple(BaseModel):
    movieId: int
    imdbId: str | None = None
    tmdbId: int | None = None

    class Config:
        orm_mode = True


class AnalyticsResponse(BaseModel):
    total_movies: int
    total_ratings: int
    average_rating: float
    total_tags: int
    total_links: int

    class Config:
        orm_mode = True
