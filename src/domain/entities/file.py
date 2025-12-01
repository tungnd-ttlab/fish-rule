from dataclasses import dataclass
from datetime import datetime

from pydantic import HttpUrl


@dataclass
class File:
    id: int | None
    s3_key: str|None
    created_at: datetime
    updated_at: datetime | None

    def __init__(self ,id=None, s3_key: HttpUrl|None=None) -> None:
       self.id = id
       self.s3_key =str(s3_key)
       self.created_at = datetime.now()