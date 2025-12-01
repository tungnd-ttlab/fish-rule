"""Domain constants for the application"""

from typing import Final

# String length constants
EMAIL_MAX_LENGTH: Final[int] = 256
PASSWORD_HASH_MAX_LENGTH: Final[int] = 1024
S3_KEY_MAX_LENGTH: Final[int] = 500
SESSION_ID_LENGTH: Final[int] = 36  # UUID string length

# Session token constants
SESSION_TOKEN_BYTES: Final[int] = 128  # For token_urlsafe

# Pagination constants
DEFAULT_PAGE: Final[int] = 1
DEFAULT_PAGE_SIZE: Final[int] = 10
MAX_PAGE_SIZE: Final[int] = 100
MIN_PAGE: Final[int] = 1
MIN_PAGE_SIZE: Final[int] = 1

# Repository constants
DEFAULT_SKIP: Final[int] = 0
DEFAULT_LIMIT: Final[int] = 100

# Query constants
SINGLE_RESULT_LIMIT: Final[int] = 1
SINGLE_RESULT_OFFSET: Final[int] = 0

# Password validation
PASSWORD_MIN_LENGTH: Final[int] = 8

