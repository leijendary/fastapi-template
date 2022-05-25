from dataclasses import dataclass
from typing import Dict

from botocore.response import StreamingBody


@dataclass
class FileStream:
    body: StreamingBody
    headers: Dict[str, str]
    media_type: str
