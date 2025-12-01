from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from application import exceptions as app_exc
from domain import exceptions as domain_exc
from domain.constants import PASSWORD_MIN_LENGTH
from infrastructure import exceptions as infra_exc
from presentation.constants import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(domain_exc.UserNotActiveError)
    async def user_not_active_handler(_: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_403_FORBIDDEN,
            content={"detail": "User is not active"},
        )

    @app.exception_handler(app_exc.UserAlreadyExistsError)
    async def user_already_exists_handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(app_exc.InvalidCredentialsError)
    async def invalid_credentials_handler(_: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid credentials."},
        )

    @app.exception_handler(app_exc.InvalidPasswordError)
    def invalid_password_handler(_: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_403_FORBIDDEN,
            content={
                "detail": (
                    f"Password should have at least one number, one letter,"
                    f" consists of at least {PASSWORD_MIN_LENGTH} symbols."
                )
            },
        )

    @app.exception_handler(infra_exc.AuthenticationError)
    async def authentication_exception_handler(
        _: Request, __: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid username or password."},
        )

    @app.exception_handler(app_exc.LogInError)
    async def login_exception_handler(_: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"detail": "You are already authenticated"},
        )

    @app.exception_handler(app_exc.AuthenticationRequiredError)
    async def authentication_required_handler(
        _: Request, __: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"detail": "Authentication required to perform this action"},
        )

    @app.exception_handler(app_exc.NotFoundError)
    async def not_found_handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )