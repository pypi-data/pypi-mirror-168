from dataclasses import dataclass, asdict

from wrapzor.errors.credentials import Message
from wrapzor.logs import logs


@dataclass
class Credentials:
    client_id: str | None
    client_secret: str | None
    code: str | None = None

    def __post_init__(self):
        _min_length: int = 10

        if self.code is not None and len(self.code) < _min_length:
            logs.warning(Message.too_small_code.value)

        if self.client_id is None:
            raise ValueError(Message.missing_client_id.value)
        if len(self.client_id) < _min_length:
            logs.warning(Message.too_small_client_id.value)

        if self.client_secret is None:
            raise ValueError(Message.missing_client_secret.value)
        if len(self.client_secret) < _min_length:
            logs.warning(Message.too_small_client_secret.value)

    def to_dict(self):
        return asdict(self)
