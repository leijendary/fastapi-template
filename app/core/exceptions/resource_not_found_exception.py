from typing import Any


class ResourceNotFoundException(Exception):
    resource: str
    identifier: Any

    def __init__(self, resource: str, identifier: Any, *args) -> None:
        super().__init__(*args)

        self.resource = resource
        self.identifier = str(identifier)
