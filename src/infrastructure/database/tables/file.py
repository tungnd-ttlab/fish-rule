from sqlalchemy import String, Table, Column, Integer, UUID
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from domain.entities.file import File
from domain.constants import S3_KEY_MAX_LENGTH
from infrastructure.database.tables.base import metadata, mapper_registry

files_table = Table(
    "files",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", UUID(as_uuid=True), nullable=True),  # No foreign key constraint for free join
    Column("s3_key", String(S3_KEY_MAX_LENGTH), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), nullable=False, onupdate=func.now()),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
)

def map_files_table() -> None:
    mapper_registry.map_imperatively(File, files_table)
