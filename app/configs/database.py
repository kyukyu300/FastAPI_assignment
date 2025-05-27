
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.configs import Config

TORTOISE_APP_MODELS = [
    "app.models.users",
    "app.models.movies",
    "aerich.models",
]

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": Config.MYSQL_HOST,
                "port": Config.MYSQL_PORT,
                "user": Config.MYSQL_USER,
                "password": Config.MYSQL_PASSWORD,
                "database": Config.MYSQL_DB,
                "connect_timeout": Config.MYSQL_CONNECT_TIMEOUT,
                "maxsize": Config.CONNECTION_POOL_MAXSIZE,
            },
        },
    },
    "apps": {
        "models": {
            "models": TORTOISE_APP_MODELS,
        },
    },
    "timezone": "Asia/Seoul",
}


def initialize_tortoise(app: FastAPI) -> None:
    Tortoise.init_models(TORTOISE_APP_MODELS, "models")
    register_tortoise(app, config=TORTOISE_ORM)