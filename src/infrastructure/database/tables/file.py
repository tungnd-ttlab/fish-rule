from sqlalchemy import String, Table, Column, Integer
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from domain.entities.file import File
from infrastructure.database.tables.base import metadata, mapper_registry

files_table = Table(
    "files",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("s3_key", String(500), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), nullable=False , onupdate=func.now()),
)

def map_files_table() -> None:
    mapper_registry.map_imperatively(File, files_table)
