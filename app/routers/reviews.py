from typing import Annotated

from fastapi import APIRouter, Form, UploadFile, File, Depends, Path, HTTPException

from app.models.reviews import Review
from app.models.users import User
from app.routers.movies import movie_router
from app.routers.users import user_router
from app.schemas.reviews import ReviewResponse
from app.utils.auth import get_current_user
from app.utils.file import upload_file, delete_file

review_router = APIRouter(prefix="/reviews", tags=["reviews"])


@review_router.post("", status_code=201)
async def create_movie_review(
        user: Annotated[User, Depends(get_current_user)],
        movie_id: int = Form(),
        title: str = Form(),
        content: str = Form(),
        review_image: UploadFile | None = File(None),
) -> ReviewResponse:
    data = {"user_id": user.id, "movie_id": movie_id, "title": title, "content": content}

    if review_image:
        data["review_image_url"] = await upload_file(review_image, "reviews/images")

    review = await Review.create(**data)

    return ReviewResponse(
        id=review.id,
        user_id=review.user_id if hasattr(review, "user_id") else user.id,
        movie_id=review.movie_id if hasattr(review, "movie_id") else movie_id,
        title=review.title,
        content=review.content,
        review_image_url=review.review_image_url,
    )


@review_router.get("/{review_id}")
async def get_review(review_id: int = Path(gt=0)) -> ReviewResponse:
    review = await Review.get_or_none(id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review does not exist")
    return ReviewResponse(
        id=review.id,
        user_id=review.user_id,
        movie_id=review.movie_id,
        title=review.title,
        content=review.content,
        review_image_url=review.review_image_url,
    )


@review_router.patch("/{review_id}")
async def update_review(
        user: Annotated[User, Depends(get_current_user)],
        update_title: str | None = None,
        update_content: str | None = None,
        update_image: UploadFile | None = File(None),
        review_id: int = Path(gt=0),
) -> ReviewResponse:
    review = await Review.get_or_none(id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review does not exist")

    if review.user_id != user.id:
        raise HTTPException(status_code=403, detail="Only the review owner can update reviews")

    review.title = update_title if update_title is not None else review.title
    review.content = update_content if update_content is not None else review.content
    if update_image:
        prev_image_url = review.review_image_url
        review.review_image_url = await upload_file(update_image, "reviews/images")

        if prev_image_url is not None:
            delete_file(prev_image_url)

    await review.save()

    return ReviewResponse(
        id=review.id,
        user_id=review.user_id,
        movie_id=review.movie_id,
        title=review.title,
        content=review.content,
        review_image_url=review.review_image_url,
    )


@review_router.delete("/{review_id}", status_code=204)
async def delete_review(
        user: Annotated[User, Depends(get_current_user)],
        review_id: int = Path(gt=0)
) -> None:
    review = await Review.get_or_none(id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review does not exist")

    if review.user_id != user.id:
        raise HTTPException(status_code=403, detail="Only the review owner can delete review.")

    await review.delete()


@movie_router.get("/{movie_id}/reviews")
async def get_movie_reviews(movie_id: int = Path(gt=0)) -> list[ReviewResponse]:
    reviews = await Review.filter(movie_id=movie_id).all()
    return [
        ReviewResponse(
            id=review.id,
            user_id=review.user_id,
            movie_id=review.movie_id,
            title=review.title,
            content=review.content,
            review_image_url=review.review_image_url
        )
        for review in reviews
    ]


@user_router.get("/me/reviews")
async def get_my_reviews(user: Annotated[User, Depends(get_current_user)]) -> list[ReviewResponse]:
    reviews = await Review.filter(user_id=user.id).all()
    return [
        ReviewResponse(
            id=review.id,
            user_id=review.user_id,
            movie_id=review.movie_id,
            title=review.title,
            content=review.content,
            review_image_url=review.review_image_url
        )
        for review in reviews
    ]