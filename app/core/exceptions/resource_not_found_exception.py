from dataclasses import dataclass
from typing import Any


@dataclass
class ResourceNotFoundException(Exception):
    resource: str
    identifier: Any
