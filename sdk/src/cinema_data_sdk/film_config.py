import os

from dotenv import load_dotenv

load_dotenv()


class MovieConfig:
    """Configuration class for movie-related settings."""

    movie_base_url: str
    movie_backoff: bool
    movie_backoff_max_time: int = 30

    def __init__(
        self,
        movie_base_url: str = None,
        movie_backoff: bool = True,
        movie_backoff_max_time: int = 30,
    ):
        """Initialize the MovieConfig class.

        Parameters
        ----------
        movie_base_url : str | None, optional
            The base URL for movie-related API calls, by default None
        movie_backoff : bool, optional
            Whether to enable backoff for API calls, by default True
        movie_backoff_max_time : int, optional
            The maximum backoff time for API calls in seconds, by default 30
        """
        self.movie_base_url = movie_base_url or os.getenv("MOVIE_API_BASE_URL")
        print(f"MOVIE_API_BASE_URL in MovieConfig init: {self.movie_base_url}")

        if not self.movie_base_url:
            raise ValueError("MOVIE_API_BASE_URL environment variable is not set.")

        self.movie_backoff = movie_backoff
        self.movie_backoff_max_time = movie_backoff_max_time

    def __str__(self) -> str:
        "Function string representation of the MovieConfig class."
        return (
            f"{self.movie_base_url} {self.movie_backoff} {self.movie_backoff_max_time}"
        )
