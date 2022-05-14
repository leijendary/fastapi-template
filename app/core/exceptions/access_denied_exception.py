from typing import List


class AccessDeniedException(Exception):
    reason: str
    scopes: List[str]
    sources: List[str]

    def __init__(
        self,
        reason: str,
        scopes: List[str] = [],
        sources: List[str] = []
    ) -> None:
        super().__init__(reason, scopes, sources)

        self.reason = reason
        self.scopes = scopes
        self.sources = sources
