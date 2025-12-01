from secrets import token_urlsafe

from application.interfaces.session_generator import SessionIdGenerator
from domain.constants import SESSION_TOKEN_BYTES


class SessionIdGeneratorImpl(SessionIdGenerator):
    def __call__(self) -> str:
        return token_urlsafe(SESSION_TOKEN_BYTES)
