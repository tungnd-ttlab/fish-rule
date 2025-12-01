from sqlalchemy import String, Table, Column, Boolean, UUID, DateTime

from domain.entities.user import User
from domain.constants import EMAIL_MAX_LENGTH, PASSWORD_HASH_MAX_LENGTH
from infrastructure.database.tables.base import metadata, mapper_registry

users_table = Table(
    "users",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("email", String(EMAIL_MAX_LENGTH), unique=True, nullable=False),
    Column("hashed_password", String(PASSWORD_HASH_MAX_LENGTH), nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
)


def map_users_table() -> None:
    mapper_registry.map_imperatively(User, users_table)
