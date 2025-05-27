
from typing import Annotated, Any

from pydantic import BaseModel, Field

from app.models.movies import GenreEnum


class CreateMovieRequest(BaseModel):
	title: str
	plot: str
	cast: dict[str, Any]
	playtime: int
	genre: GenreEnum


class MovieResponse(BaseModel):
	id: int
	title: str
	playtime: int
	plot: str
	cast: dict[str, Any]
	genre: GenreEnum


class MovieSearchParams(BaseModel):
	title: str | None = None
	genre: GenreEnum | None = None
	plot: str | None = None
	cast: dict[str, Any] | None = None


class MovieUpdateRequest(BaseModel):
	title: str | None = None
	genre: GenreEnum | None = None
	plot: str | None = None
	cast: dict[str, Any] | None = None
	playtime: Annotated[int, Field(gt=0)] | None = None