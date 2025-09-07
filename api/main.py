import query_helpers as helpers
import schemas
from database import SessionLocal
from fastapi import Depends, FastAPI, HTTPException, Path, Query
from sqlalchemy.orm import Session

api_description = """

Bienvenue sur l'API MovieLens!

Cette API permet d'accéder aux données de films, notes et tags provenant du dataset [MovieLens](https://grouplens.org/datasets/movielens/).

### Fonctionnalités de l'API

- Rechercher un film par son ID ou lister tous les films
- Consulter les évaluations (ratings) par utilisateur et/ou film
- Accéder aux tags associés aux films par les utilisateurs
- Obtenir des liens externes (IMDB, TMDB) pour chaque film
- Voir des statistiques globales sur le dataset

Tous les endpoints supportent la pagination et certains permettent des filtres avancés.

"""
# --- Initialisation de l'application FastAPI ---
app = FastAPI(title="MovieLens API", description=api_description, version="0.1")


# --- Dépendance pour obtenir une session de base de données ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Endpoints pour tester la sanité de l'API ---
@app.get(
    "/",
    tags=["Sanity Check"],
    summary="Sanity Check",
    description="Endpoint de test pour vérifier que l'API fonctionne.",
    response_description="Message de succès",
    operation_id="sanity_check_movies_api",
)
async def root():
    return {"message": "MovieLens API is up and running!"}


@app.get(
    "/movies/{movie_id}",  # /movies/1
    summary="Get Movie by ID",
    description="Retrieve a movie by its ID.",
    response_description="Movie details",
    response_model=schemas.MovieDetailed,
    tags=["Movies"],
)
def read_movie(
    movie_id: int = Path(..., description="The ID of the movie to retrieve"),
    db: Session = Depends(get_db),
):
    db_movie = helpers.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(
            status_code=404, detail=f"Movie with ID {movie_id} not found"
        )
    return db_movie


# -- Endpoint pour récupérer une liste de films avec pagination et filtres ---
@app.get(
    "/movies/",
    summary="Get list of Movies",
    description="Retrieve a list of movies with optional pagination and filters.",
    response_description="List of movies",
    response_model=list[schemas.MovieSimple],
    tags=["Movies"],
)
def list_movies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, gt=0, description="Number of records to return"),
    title: str | None = Query(None, description="Filter by movie title"),
    genre: str | None = Query(None, description="Filter by movie genre"),
    db: Session = Depends(get_db),
):
    movies = helpers.get_movies(db, skip=skip, limit=limit, title=title, genre=genre)
    return movies


# --- Endpoints pour les notes (ratings) ---
@app.get(
    "/ratings/{user_id}/{movie_id}",
    summary="Get Rating by User ID and Movie ID",
    description="Retrieve a rating by user ID and movie ID.",
    response_description="Rating details",
    response_model=schemas.RatingSimple,
    tags=["Ratings"],
)
def read_rating(
    user_id: int = Path(..., description="The ID of the user"),
    movie_id: int = Path(..., description="The ID of the movie"),
    db: Session = Depends(get_db),
):
    rating = helpers.get_rating(db, user_id=user_id, movie_id=movie_id)
    if rating is None:
        raise HTTPException(
            status_code=404,
            detail=f"Rating for User ID {user_id} and Movie ID {movie_id} not found",
        )
    return rating


@app.get(
    "/ratings/",
    summary="Get list of Ratings",
    description="Retrieve a list of ratings with optional pagination and filters.",
    response_description="List of ratings",
    response_model=list[schemas.RatingSimple],
    tags=["Ratings"],
)
def list_ratings(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, gt=0, description="Number of records to return"),
    movie_id: int | None = Query(None, description="Filter by movie ID"),
    user_id: int | None = Query(None, description="Filter by user ID"),
    min_rating: float | None = Query(
        None, ge=0, le=5, description="Filter by minimum rating value"
    ),
    db: Session = Depends(get_db),
):
    ratings = helpers.get_ratings(
        db,
        skip=skip,
        limit=limit,
        movie_id=movie_id,
        user_id=user_id,
        min_rating=min_rating,
    )
    return ratings


@app.get(
    "/tags/{user_id}/{movie_id}/{tag_text}",
    summary="Get Tag by User ID, Movie ID, and Tag Text",
    description="Retrieve a tag by user ID, movie ID, and tag text.",
    response_description="Tag details",
    response_model=schemas.TagSimple,
    tags=["Tags"],
)
def read_tag(
    user_id: int = Path(..., description="The ID of the user"),
    movie_id: int = Path(..., description="The ID of the movie"),
    tag_text: str = Path(..., description="The text of the tag"),
    db: Session = Depends(get_db),
):
    tag = helpers.get_tag(db, user_id=user_id, movie_id=movie_id, tag_text=tag_text)
    if tag is None:
        raise HTTPException(
            status_code=404,
            detail=f"Tag '{tag_text}' for User ID {user_id} and Movie ID {movie_id} not found",
        )
    return tag


@app.get(
    "/tags/",
    summary="Get list of Tags",
    description="Retrieve a list of tags with optional pagination and filters.",
    response_description="List of tags",
    response_model=list[schemas.TagSimple],
    tags=["Tags"],
)
def list_tags(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, gt=0, description="Number of records to return"),
    movie_id: int | None = Query(None, description="Filter by movie ID"),
    user_id: int | None = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db),
):
    tags = helpers.get_tags(
        db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id
    )
    return tags


# --- Endpoints pour les liens (links) ---
@app.get(
    "/links/{movie_id}",
    summary="Get Link by Movie ID",
    description="Retrieve a link by movie ID.",
    response_description="Link details",
    response_model=schemas.LinkSimple,
    tags=["Links"],
)
def read_link(
    movie_id: int = Path(..., description="The ID of the movie"),
    db: Session = Depends(get_db),
):
    link = helpers.get_link(db, movie_id=movie_id)
    if link is None:
        raise HTTPException(
            status_code=404, detail=f"Link for Movie ID {movie_id} not found"
        )
    return link


@app.get(
    "/links/",
    summary="Get list of Links",
    description="Retrieve a list of links with optional pagination.",
    response_description="List of links",
    response_model=list[schemas.LinkSimple],
    tags=["Links"],
)
def list_links(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, gt=0, description="Number of records to return"),
    db: Session = Depends(get_db),
):
    links = helpers.get_links(db, skip=skip, limit=limit)
    return links


# --- Endpoints pour les statistiques ---
@app.get(
    "/analytics/",
    summary="Get Dataset Analytics including counts of movies, ratings, tags, and links",
    description="Retrieve Analytics about the dataset, including counts of movies, ratings, tags, and links.",
    response_description="Dataset analytics",
    response_model=schemas.AnalyticsResponse,
    tags=["Analytics"],
)
def get_stats(db: Session = Depends(get_db)):
    total_movies = helpers.get_movie_count(db)
    total_ratings = helpers.get_rating_count(db)
    average_rating = helpers.get_average_rating(db)
    total_tags = helpers.get_tag_count(db)
    total_links = helpers.get_link_count(db)
    return {
        "total_movies": total_movies,
        "total_ratings": total_ratings,
        "average_rating": average_rating,
        "total_tags": total_tags,
        "total_links": total_links,
    }
