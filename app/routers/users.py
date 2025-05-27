from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, Query, APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.users import User
from app.schemas.users import UserUpdateRequest, UserCreateRequest, UserSearchParams, Token, UserResponse
from app.utils.auth import authenticate, get_current_user, hash_password
from app.utils.jwt import create_access_token

user_router = APIRouter(prefix='/users', tags=["users"])


@user_router.post('')
async def create_user(data: UserCreateRequest):
	data = data.model_dump()
	data['hashed_password'] = hash_password(data.pop('password'))
	user = await User.create(**data)
	return user.id


@user_router.get('')
async def get_all_users() -> list[UserResponse]:
	result = await User.filter().all()
	if not result:
		raise HTTPException(status_code=404)
	return result


@user_router.post('/login', response_model=Token)
async def login_user(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
	user = await authenticate(data.username, data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token = create_access_token(data={"user_id": user.id})
	user.last_login = datetime.now()
	await user.save()
	return Token(access_token=access_token, token_type="bearer")


@user_router.get('/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]) -> list[UserResponse]:
	valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
	filtered_users = await User.filter(**valid_query).all()
	if not filtered_users:
		raise HTTPException(status_code=404)
	return filtered_users


@user_router.get('/me')
async def get_user(user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
	return UserResponse(id=user.id, username=user.username, age=user.age, gender=user.gender)


@user_router.patch('/me')
async def update_user(
	user: Annotated[User, Depends(get_current_user)],
	data: UserUpdateRequest,
) -> UserResponse:
	update_data = {key: value for key, value in data.model_dump().items() if value is not None}
	if 'password' in update_data.keys():
		update_data['hashed_password'] = hash_password(update_data.pop('password'))
	user = await user.update_from_dict(data=update_data)
	await user.save()
	return UserResponse(id=user.id, username=user.username, age=user.age, gender=user.gender)


@user_router.delete('/me')
async def delete_user(user: Annotated[User, Depends(get_current_user)],):
	await user.delete()
	return {'detail': 'Successfully Deleted.'}
