from typing import List


class AccessDeniedException(Exception):
    reason: str
    scopes: List[str]
