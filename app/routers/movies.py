# movies route
from typing import Annotated
from fastapi import HTTPException

from fastapi import APIRouter, Query, Path

from app.models.movies import MovieModel
from app.schemas.movies import MovieResponse, CreateMovieRequest, MovieSearchParams, MovieUpdateRequest

movie_router = APIRouter(prefix="/movies", tags=["movie"])

@movie_router.post("/movies", response_model=MovieResponse, status_code=201)
async def create_movies(data: CreateMovieRequest):
    movie = MovieModel.create(**data.model_dump())
    return movie

@movie_router.get('/movies', response_model=list[MovieResponse], status_code = 200)
async def get_movies(query_params: Annotated[MovieSearchParams, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}

    if valid_query:
        return MovieModel.filter(**valid_query)

    return MovieModel.all()

@movie_router.get('/movies/{movie_id}', response_model=MovieResponse, status_code=200)
async def get_movie(movie_id: int = Path (gt=0)):
    movie = MovieModel.get(id = movie_id)
    if movie is None:
        raise HTTPException(status_code = 404)
    return movie

@movie_router.patch('/movies/{movie_id}', response_model=MovieResponse, status_code=200)
async def update_movie(data: MovieUpdateRequest, movie_id: int = Path(gt=0)):
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code = 404)
    movie.update(**data.model_dump())
    return movie

@movie_router.delete('/movies/{movie_id}')
async def delete_movie(movie_id: int = Path(gt=0)):
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404)
    movie.delete()
    return