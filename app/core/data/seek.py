import json
from base64 import b64encode, b64decode
from datetime import datetime
from typing import Generic, TypeVar, List, Optional

from pydantic.fields import Field
from pydantic.main import BaseModel

from app.core.constants import UTF_8
from app.core.libraries.message import get_message
from app.core.security.encryption import encrypt, decrypt
from app.core.utils.dict_util import to_dict

T = TypeVar("T")


class Seek(BaseModel, Generic[T]):
    content: List[T] = Field(..., title=get_message("document.seek_content"))
    size: int = Field(..., title=get_message("document.seek_size"))
    limit: int = Field(..., title=get_message("document.seek_limit"))
    next_token: Optional[str] = Field(
        None,
        title=get_message("document.seek_next_token")
    )

    @classmethod
    def create(
            cls,
            content: List[T],
            next_token: Optional[str],
            size: int,
            limit: int
    ):
        cls.content = content
        cls.next_token = next_token
        cls.size = size
        cls.limit = limit

        return cls(
            content=content,
            next_token=next_token,
            size=size,
            limit=limit
        )


class SeekToken:
    def __init__(self, created_at: datetime, row_id: int):
        self.created_at = created_at
        self.row_id = row_id

    @classmethod
    def from_token(cls, next_token: str):
        decoded = b64decode(next_token).decode(UTF_8)
        decrypted = decrypt(decoded)
        loaded = json.loads(decrypted)

        return cls(**loaded)

    def next_token(self) -> str:
        d = to_dict(self)
        json_str = json.dumps(d)
        encrypted = encrypt(json_str)
        encoded = encrypted.encode(UTF_8)

        return b64encode(encoded).decode(UTF_8)
