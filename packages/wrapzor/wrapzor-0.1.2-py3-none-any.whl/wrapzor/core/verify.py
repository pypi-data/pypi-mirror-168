import json
from typing import Callable, Awaitable, Coroutine, Any, Type

from httpx import Response, codes
from pydantic import BaseModel

from wrapzor.errors.api import ArgsError, Message


def verify_data(
    input_model: Type[BaseModel] | None = None,
    output_model: Type[BaseModel] | None = None,
):
    def function_verify_data(
        f: Callable[..., Awaitable[Response]]
    ) -> Callable[..., Coroutine[Any, Any, output_model | Response]]:
        async def wrapper(*args, **kwargs) -> output_model | Response:
            if input_model is not None:
                if "data" in kwargs:

                    data = kwargs["data"]
                    del kwargs["data"]
                    if not isinstance(data, dict):
                        raise TypeError("Argument data must be a dict")

                    _ = input_model(**data)
                    response = await f(*args, **kwargs, data=json.dumps(data))
                elif "params" in kwargs:

                    params = kwargs["params"]
                    del kwargs["params"]
                    if not isinstance(params, dict):
                        raise TypeError("Argument params must be a dict")

                    _ = input_model(**params)

                    response = await f(*args, **kwargs, params=params)
                else:
                    raise ArgsError(Message.input_data_missing)

            else:
                response = await f(*args, **kwargs)

            if output_model is not None and response.status_code != codes.NO_CONTENT:
                response_data = response.json()
                if not isinstance(response_data, dict):
                    raise TypeError("Response json -data- must be a dict")
                return output_model(**response_data)
            else:
                return response

        return wrapper

    return function_verify_data
