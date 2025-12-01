from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from application.interactors.login_user import (
    LoginResponse,
    LoginUserInteractor,
    LoginUserRequest,
)
from application.interactors.logout_user import LogoutUserInteractor
from application.interactors.register_user import (
    RegisterUserInteractor,
    RegisterUserRequest,
    RegisterUserResponse,
)
from presentation.constants import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_409_CONFLICT,
    ERROR_UNAUTHORIZED,
    ERROR_INVALID_CREDENTIALS,
    ERROR_USER_NOT_ACTIVE,
    ERROR_USER_ALREADY_EXISTS,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    status_code=HTTP_201_CREATED,
    responses={
        HTTP_409_CONFLICT: {"description": ERROR_USER_ALREADY_EXISTS},
    },
)
@inject
async def register(
    data: RegisterUserRequest,
    register_user: FromDishka[RegisterUserInteractor],
) -> RegisterUserResponse:
    return await register_user(data)


@router.post(
    "/login",
    status_code=HTTP_200_OK,
    responses={
        HTTP_401_UNAUTHORIZED: {"description": ERROR_INVALID_CREDENTIALS},
        HTTP_403_FORBIDDEN: {"description": ERROR_USER_NOT_ACTIVE},
    },
)
@inject
async def login(
    data: LoginUserRequest, login_user: FromDishka[LoginUserInteractor]
) -> LoginResponse:
    return await login_user(data)


@router.post(
    "/logout",
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_401_UNAUTHORIZED: {"description": ERROR_UNAUTHORIZED},
    },
)
@inject
async def logout(logout_user: FromDishka[LogoutUserInteractor]) -> None:
    return await logout_user()
