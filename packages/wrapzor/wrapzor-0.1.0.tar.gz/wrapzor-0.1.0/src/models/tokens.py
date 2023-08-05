from dataclasses import dataclass, asdict


@dataclass
class Token:
    access_token: str
    api_domain: str
    token_type: str
    expires_in: int
    refresh_token: str | None = None

    def to_dict(self):
        return asdict(self)
