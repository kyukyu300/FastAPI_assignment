
from tortoise import Model, fields

from app.models.base import BaseModel


class ReviewLike(BaseModel, Model):
    user = fields.ForeignKeyField("models.User", related_name="review_likes")
    review = fields.ForeignKeyField("models.Review", related_name="likes")
    is_liked = fields.BooleanField(default=True)

    class Meta:
        table = "review_likes"
        unique_together = (("user", "review"),)