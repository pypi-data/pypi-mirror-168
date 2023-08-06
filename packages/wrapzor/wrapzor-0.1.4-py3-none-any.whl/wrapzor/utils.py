from datetime import datetime

from httpx import URL

from wrapzor.errors.api import Message


def clean_domain(domain: str | URL, return_str: bool = False) -> URL | str:
    _domain = str(domain)
    if _domain[:4] != "http":
        raise ValueError(Message.bad_domain.value)
    while _domain[-1] == "/":
        _domain = _domain[:-1]
    return _domain if return_str else URL(_domain)


def top_level_domain(domain: str | URL) -> str:
    _domain = str(domain)
    return _domain.split(".")[-1]


def now_str():
    return str(datetime.utcnow()).replace(" ", "T")
