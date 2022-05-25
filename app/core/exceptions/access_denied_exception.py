from dataclasses import dataclass
from typing import List


@dataclass
class AccessDeniedException(Exception):
    reason: str
    scopes: List[str]
    sources: List[str]
