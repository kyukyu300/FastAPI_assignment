
from typing import Annotated

from fastapi import Query, Path, HTTPException, APIRouter

from app.models.movies import Movie
from app.schemas.movies import MovieResponse, CreateMovieRequest, MovieSearchParams, MovieUpdateRequest


movie_router = APIRouter(prefix="/movies", tags=["movies"])


@movie_router.post('', response_model=MovieResponse, status_code=201)
async def create_movie(data: CreateMovieRequest):
	movie = await Movie.create(**data.model_dump())
	return movie


@movie_router.get('', response_model=list[MovieResponse], status_code=200)
async def get_movies(query_params: Annotated[MovieSearchParams, Query()]):
	valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
	return await Movie.filter(**valid_query).all()


@movie_router.get('/{movie_id}', response_model=MovieResponse, status_code=200)
async def get_movie(movie_id: int = Path(gt=0)):
	movie = await Movie.get_or_none(id=movie_id)
	if movie is None:
		raise HTTPException(status_code=404)
	return movie


@movie_router.patch('/{movie_id}', response_model=MovieResponse, status_code=200)
async def edit_movie(data: MovieUpdateRequest, movie_id: int = Path(gt=0)):
	movie = await Movie.get_or_none(id=movie_id)
	if movie is None:
		raise HTTPException(status_code=404)
	valid_params = {key: value for key, value in data.model_dump().items() if value is not None}
	await movie.update_from_dict(valid_params)
	await movie.save()
	return movie


@movie_router.delete('/{movie_id}', status_code=204)
async def delete_movie(movie_id: int = Path(gt=0)):
	movie = await Movie.get(id=movie_id)
	if movie is None:
		raise HTTPException(status_code=404)
	await movie.delete()
	return
