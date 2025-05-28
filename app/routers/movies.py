
from typing import Annotated

from fastapi import Query, Path, HTTPException, APIRouter, UploadFile

from app.models.movies import Movie
from app.schemas.movies import MovieResponse, CreateMovieRequest, MovieSearchParams, MovieUpdateRequest
from app.utils.file import validate_image_extension, upload_file, delete_file

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


@movie_router.post("/{movie_id}/poster_image", response_model=MovieResponse, status_code=201)
async def register_poster_image(image: UploadFile, movie_id: int = Path(gt=0)):
	validate_image_extension(image)

	movie = await Movie.get_or_none(id=movie_id)
	if not movie:
		raise HTTPException(status_code=404, detail="Movie not found")

	prev_image_url = movie.poster_image_url
	try:
		image_url = await upload_file(image, "movies/poster_images")
		movie.poster_image_url = image_url
		await movie.save()

		if prev_image_url is not None:
			delete_file(prev_image_url)

		return movie
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")