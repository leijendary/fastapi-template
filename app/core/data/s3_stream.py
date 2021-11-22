from typing import Dict

from botocore.response import StreamingBody


class S3FileStream:
    body: StreamingBody
    headers: Dict[str, str]
    media_type: str

    def __init__(
        self,
        body: StreamingBody,
        headers: Dict[str, str],
        media_type: str
    ):
        self.body = body
        self.headers = headers
        self.media_type = media_type
