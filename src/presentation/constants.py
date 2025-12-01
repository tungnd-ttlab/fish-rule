"""Presentation layer constants"""

from typing import Final
from starlette import status

# HTTP Status Codes
HTTP_200_OK: Final[int] = status.HTTP_200_OK
HTTP_201_CREATED: Final[int] = status.HTTP_201_CREATED
HTTP_204_NO_CONTENT: Final[int] = status.HTTP_204_NO_CONTENT
HTTP_400_BAD_REQUEST: Final[int] = status.HTTP_400_BAD_REQUEST
HTTP_401_UNAUTHORIZED: Final[int] = status.HTTP_401_UNAUTHORIZED
HTTP_403_FORBIDDEN: Final[int] = status.HTTP_403_FORBIDDEN
HTTP_404_NOT_FOUND: Final[int] = status.HTTP_404_NOT_FOUND
HTTP_409_CONFLICT: Final[int] = status.HTTP_409_CONFLICT

# Error messages
ERROR_BAD_REQUEST: Final[str] = "Bad Request"
ERROR_UNAUTHORIZED: Final[str] = "Authentication required"
ERROR_INVALID_CREDENTIALS: Final[str] = "Invalid username or password"
ERROR_USER_NOT_ACTIVE: Final[str] = "User is not active"
ERROR_USER_ALREADY_EXISTS: Final[str] = "User already exists"

