from enum import StrEnum

from tortoise import Model, fields

from app.models.base import BaseModel


class GenreEnum(StrEnum):
    SF = "SF"
    ADVENTURE = "Adventure"
    ROMANCE = "Romance"
    COMIC = "Comic"
    FANTASY = "Fantasy"
    SCIENCE = "Science"
    MYSTERY = "Mystery"
    ACTION = "Action"
    HORROR = "Horror"


class Movie(BaseModel, Model):
    title = fields.CharField(max_length=255)
    plot = fields.TextField()
    cast = fields.JSONField()
    playtime = fields.IntField()
    genre = fields.CharEnumField(GenreEnum)

    class Meta:
        table = "movies"