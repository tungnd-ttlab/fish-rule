import re

from domain.constants import PASSWORD_MIN_LENGTH

# Password must contain at least one letter, one digit, and be at least PASSWORD_MIN_LENGTH characters
PASSWORD_PATTERN: re.Pattern[str] = re.compile(
    rf"^(?=.*[A-Za-z])(?=.*\d).{{{PASSWORD_MIN_LENGTH},}}$"
)


def validate_password(password: str) -> bool:
    return bool(PASSWORD_PATTERN.match(password))
