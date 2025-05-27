
from fastapi import FastAPI

from app.models.movies import MovieModel
from app.models.users import UserModel
from app.routers.movies import movie_router
from app.routers.users import user_router

app = FastAPI()

UserModel.create_dummy()  # API 테스트를 위한 더미를 생성하는 메서드 입니다.
MovieModel.create_dummy()

app.include_router(user_router)
app.include_router(movie_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
