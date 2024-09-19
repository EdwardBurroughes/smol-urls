import json
from urllib.parse import urlparse

import attrs


class MalformedPayload(Exception):
    pass


@attrs.frozen
class ShortenUrl:
    url: str = attrs.field()

    @url.validator
    def validate_url(self, _, value: str):
        result = urlparse(value)
        return all([result.scheme, result.netloc])

    @classmethod
    def deserialise(cls, data: bytes) -> "ShortenUrl":
        try:
            data = json.loads(data)
            return cls(**data)
        except (TypeError, ValueError) as e:
            raise MalformedPayload(data) from e
