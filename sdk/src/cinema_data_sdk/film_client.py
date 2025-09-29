from typing import Literal, Union

import httpx
import pandas as pd

from .film_config import MovieConfig
from .schemas import (
    AnalyticsResponse,
    LinkSimple,
    MovieDetailed,
    MovieSimple,
    RatingSimple,
    TagSimple,
)


class MovieClient:
    """Client class for interacting with the movie API."""

    def __init__(self, config: MovieConfig):
        """Initialize the MovieClient class.

        Parameters
        ----------
        config : MovieConfig
            An instance of the MovieConfig class containing configuration settings.
        """
        self.config = config or MovieConfig()
        self.base_url = self.config.movie_base_url

    def _format_output(
        self, data: dict, model, output_format: Literal["pydantic", "dict", "pandas"]
    ):
        """Format the output data based on the specified format.

        Parameters
        ----------
        data : dict
            The data to format.
        model : BaseModel
            The Pydantic model to use for formatting.
        output_format : Literal["pydantic", "dict", "pandas"]
            The desired output format.

        Returns
        -------
        Union[BaseModel, dict, pd.DataFrame]
            The formatted data.
        """
        if output_format == "pydantic":
            return [model(**item) for item in data]
        elif output_format == "dict":
            return data
        elif output_format == "pandas":
            import pandas as pd

            return pd.DataFrame(data)
        else:
            raise ValueError(
                "Invalid output format. Choose from 'pydantic', 'dict', or 'pandas'."
            )

    def health_check(self) -> dict:
        """Perform a health check on the movie API.

        Returns
        -------
        dict
            A dictionary containing the health status of the API.

        Raises
        ------
        httpx.HTTPStatusError
            If the HTTP request returns an unsuccessful status code.
        """
        url = f"{self.base_url}/"
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()

    def get_movie(self, movie_id: int) -> MovieDetailed:
        """Retrieve a movie by its ID.

        Parameters
        ----------
        movie_id : int
            The ID of the movie to retrieve.

        Returns
        -------
        MovieDetailed
            An instance of MovieDetailed containing movie details.

        Raises
        ------
        httpx.HTTPStatusError
            If the HTTP request returns an unsuccessful status code.
        """
        url = f"{self.base_url}/movies/{movie_id}"
        response = httpx.get(url)
        response.raise_for_status()
        return MovieDetailed(**response.json())

    def list_movies(
        self,
        skip: int = 0,
        limit: int = 10,
        title: str | None = None,
        genre: str | None = None,
        output_format: Literal["pydantic", "dict", "pandas"] = "pydantic",
    ) -> Union[list[MovieSimple], list[dict], "pd.DataFrame"]:
        """Retrieve a list of movies with optional pagination and filters.

        Parameters
        ----------
        skip : int, optional
            Number of records to skip, by default 0
        limit : int, optional
            Number of records to return, by default 10
        title : str | None, optional
            Filter by movie title, by default None
        genre : str | None, optional
            Filter by movie genre, by default None

        Returns
        -------
        list[MovieSimple]
            A list of MovieSimple instances.

        Raises
        ------
        httpx.HTTPStatusError
            If the HTTP request returns an unsuccessful status code.
        """
        url = f"{self.base_url}/movies/"
        params = {"skip": skip, "limit": limit}
        if title:
            params["title"] = title
        if genre:
            params["genre"] = genre

        response = httpx.get(url, params=params)
        response.raise_for_status()
        return self._format_output(response.json(), MovieSimple, output_format)

    def get_rating(self, user_id: int, movie_id: int) -> RatingSimple:
        """Retrieve a rating by user ID and movie ID.

        Parameters
        ----------
        user_id : int
            The ID of the user.
        movie_id : int
            The ID of the movie.

        Returns
        -------
        RatingSimple
            An instance of RatingSimple containing rating details.

        Raises
        ------
        httpx.HTTPStatusError
            If the HTTP request returns an unsuccessful status code.
        """
        url = f"{self.base_url}/ratings/{user_id}/{movie_id}"
        response = httpx.get(url)
        response.raise_for_status()
        return RatingSimple(**response.json())

    def list_ratings(
        self,
        skip: int = 0,
        limit: int = 10,
        movie_id: int | None = None,
        user_id: int | None = None,
        min_rating: float | None = None,
        output_format: Literal["pydantic", "dict", "pandas"] = "pydantic",
    ) -> Union[list[RatingSimple], list[dict], "pd.DataFrame"]:
        """Retrieve a list of ratings with optional pagination and filters.

        Parameters
        ----------
        skip : int, optional
            Number of records to skip, by default 0
        limit : int, optional
            Number of records to return, by default 10
        movie_id : int | None, optional
            Filter by movie ID, by default None
        user_id : int | None, optional
            Filter by user ID, by default None
        min_rating : float | None, optional
            Filter by minimum rating value, by default None

        Returns
        -------
        list[RatingSimple]
            A list of RatingSimple instances.

        Raises
        ------
        httpx.HTTPStatusError
            If the HTTP request returns an unsuccessful status code.
        """
        url = f"{self.base_url}/ratings/"
        params = {"skip": skip, "limit": limit}
        if movie_id:
            params["movie_id"] = movie_id
        if user_id:
            params["user_id"] = user_id
        if min_rating is not None:
            params["min_rating"] = min_rating

        response = httpx.get(url, params=params)
        response.raise_for_status()
        return self._format_output(response.json(), RatingSimple, output_format)

    def get_tag(self, user_id: int, movie_id: int, tag_text: str) -> TagSimple:
        """Retrieve a tag by user ID, movie ID, and tag text.

        Parameters
        ----------
        user_id : int
            The ID of the user.
        movie_id : int
            The ID of the movie.
        tag_text : str
            The text of the tag.

        Returns
        -------
        TagSimple
            An instance of TagSimple containing tag details.

        Raises
        ------
        httpx.HTTPStatusError
            If the HTTP request returns an unsuccessful status code.
        """
        url = f"{self.base_url}/tags/{user_id}/{movie_id}/{tag_text}"
        response = httpx.get(url)
        response.raise_for_status()
        return TagSimple(**response.json())

    def list_tags(
        self,
        skip: int = 0,
        limit: int = 10,
        movie_id: int | None = None,
        user_id: int | None = None,
        output_format: Literal["pydantic", "dict", "pandas"] = "pydantic",
    ) -> Union[list[TagSimple], list[dict], "pd.DataFrame"]:
        """Retrieve a list of tags with optional pagination and filters.

        Parameters
        ----------
        skip : int, optional
            Number of records to skip, by default 0
        limit : int, optional
            Number of records to return, by default 10
        movie_id : int | None, optional
            Filter by movie ID, by default None
        user_id : int | None, optional
            Filter by user ID, by default None

        Returns
        -------
        list[TagSimple]
            A list of TagSimple instances.

        Raises
        ------
        httpx.HTTPStatusError
            If the HTTP request returns an unsuccessful status code.
        """
        url = f"{self.base_url}/tags/"
        params = {"skip": skip, "limit": limit}
        if movie_id:
            params["movie_id"] = movie_id
        if user_id:
            params["user_id"] = user_id

        response = httpx.get(url, params=params)
        response.raise_for_status()
        return self._format_output(response.json(), TagSimple, output_format)

    def get_link(self, movie_id: int) -> LinkSimple:
        """Retrieve a link by movie ID.

        Parameters
        ----------
        movie_id : int
            The ID of the movie.

        Returns
        -------
        LinkSimple
            An instance of LinkSimple containing link details.

        Raises
        ------
        httpx.HTTPStatusError
            If the HTTP request returns an unsuccessful status code.
        """
        url = f"{self.base_url}/links/{movie_id}"
        response = httpx.get(url)
        response.raise_for_status()
        return LinkSimple(**response.json())

    def list_links(
        self,
        skip: int = 0,
        limit: int = 10,
        output_format: Literal["pydantic", "dict", "pandas"] = "pydantic",
    ) -> Union[list[LinkSimple], list[dict], "pd.DataFrame"]:
        """Retrieve a list of links with optional pagination.

        Parameters
        ----------
        skip : int, optional
            Number of records to skip, by default 0
        limit : int, optional
            Number of records to return, by default 10

        Returns
        -------
        list[LinkSimple]
            A list of LinkSimple instances.

        Raises
        ------
        httpx.HTTPStatusError
            If the HTTP request returns an unsuccessful status code.
        """
        url = f"{self.base_url}/links/"
        params = {"skip": skip, "limit": limit}

        response = httpx.get(url, params=params)
        response.raise_for_status()
        return self._format_output(response.json(), LinkSimple, output_format)

    def get_analytics(self) -> AnalyticsResponse:
        """Retrieve analytics data from the API.

        Returns
        -------
        AnalyticsResponse
            An instance of AnalyticsResponse containing analytics data.

        Raises
        ------
        httpx.HTTPStatusError
            If the HTTP request returns an unsuccessful status code.
        """
        url = f"{self.base_url}/analytics/"
        response = httpx.get(url)
        response.raise_for_status()
        return AnalyticsResponse(**response.json())
