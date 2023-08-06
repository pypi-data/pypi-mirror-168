from typing import Callable, Awaitable, Any, Coroutine

from httpx import Response, codes

from wrapzor.errors.api import InvalidStatusError
from wrapzor.logs import logs


def retry(
    max_retries: int = 5,
    expected_status_code: int | list[int] | None = None,
):
    if expected_status_code is None:
        expected_status_code = [codes.OK, codes.CREATED, codes.NO_CONTENT]

    def function_retry(
        f: Callable[..., Awaitable[Response]]
    ) -> Callable[..., Coroutine[Any, Any, Response]]:
        async def wrapper(*args, **kwargs) -> Response:

            _valid_status_codes = set(
                expected_status_code
                if isinstance(expected_status_code, list)
                else [expected_status_code]
            )

            response = await f(*args, **kwargs)
            if response.status_code in _valid_status_codes:
                return response

            # Retry part
            retries, _max_retries = 0, max(max_retries, 1)
            while (retries := retries + 1) < _max_retries:
                response = await f(*args, **kwargs)
                if response.status_code in _valid_status_codes:
                    return response

            logs.error(
                {
                    "error": f"Max retries exceeded (retries: {_max_retries})",
                    "response.status_code": response.status_code,
                    "response.content": response.json(),
                }
            )
            raise InvalidStatusError(response)

        return wrapper

    return function_retry
