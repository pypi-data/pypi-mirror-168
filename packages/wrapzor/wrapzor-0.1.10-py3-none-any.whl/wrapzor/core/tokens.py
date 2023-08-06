import json
from datetime import datetime
from typing import Callable, Awaitable, Coroutine, Any

import httpx
from httpx import Response, codes

from wrapzor.core.api import Api
from wrapzor.core.credentials import Credentials
from wrapzor.core.globals import API
from wrapzor.core.retries import retry
from wrapzor.errors.api import InvalidStatusError, ArgsError
from wrapzor.logs import logs
from wrapzor.models.tokens import Token


@retry()
async def get_refresh_token(account_domain: str, credentials: Credentials) -> Response:
    access_token_url = f"{account_domain}/oauth/v2/token"
    data = credentials.to_dict()
    data["grant_type"] = "authorization_code"
    async with httpx.AsyncClient() as client:
        response = await client.post(access_token_url, data=data)
    return response


@retry()
async def get_access_token(
    refresh_token: str, account_domain: str, credentials: Credentials
) -> Response:
    access_token_url = f"{account_domain}/oauth/v2/token"
    data = credentials.to_dict()
    data["grant_type"] = "refresh_token"
    data["refresh_token"] = refresh_token
    async with httpx.AsyncClient() as client:
        response = await client.post(access_token_url, data=data)
    return response


async def refresh_all_api_tokens(api: Api = API):
    response = await get_refresh_token(
        account_domain=api.account_domain, credentials=api.credentials
    )
    if response.status_code != codes.OK or "error" in response.json():
        logs.error(
            {
                "error": "Can't get refresh token",
                "response.status_code": response.status_code,
                "response.content": response.json(),
            }
        )
        raise InvalidStatusError(response)
    token = Token(**response.json())
    api.refresh_token = token.refresh_token
    api.access_token = token.access_token

    logs.warning(
        {
            "info": "Tokens and Auth Header have been refreshed",
            "message": "Your credentials and ZOHO_REFRESH_CODE have been saved in the credentials.txt",
        }
    )


async def refresh_access_api_token(api: Api = API):
    response = await get_access_token(
        refresh_token=api.refresh_token,
        account_domain=api.account_domain,
        credentials=api.credentials,
    )
    if response.status_code != codes.OK:
        logs.error(
            {
                "error": "Can't get access token",
                "response.status_code": response.status_code,
                "response.content": response.json(),
            }
        )
        raise InvalidStatusError(response)
    token = Token(**response.json())
    api.access_token = token.access_token
    logs.info({"info": "Access token and Auth Header have been refreshed"})


def inject_tokens(api: Api = API):
    if not isinstance(api, Api):
        raise ValueError("Please verify the api arg is a real Api object")

    def function_inject_tokens(
        f: Callable[..., Awaitable[Response]]
    ) -> Callable[..., Coroutine[Any, Any, Response]]:
        @retry()
        async def wrapper(*args, **kwargs) -> Response:
            if api.code is None and api.refresh_token is None:
                raise ArgsError(
                    "Please set either the API code or the API refresh token"
                )

            if api.refresh_token is None:
                await refresh_all_api_tokens(api)

            if api.access_token is None:
                await refresh_access_api_token(api)

            if "data" in kwargs:
                if not isinstance(kwargs["data"], dict):
                    raise TypeError("Argument data must be a dict")
                kwargs["data"] = json.dumps(kwargs["data"])
            if "params" in kwargs:
                if not isinstance(kwargs["params"], dict):
                    raise TypeError("Argument params must be a dict")

            async with httpx.AsyncClient(headers=api.auth_header) as client:
                response = await f(*args, client=client, api=api, **kwargs)

            retries, _max_retries = 0, max(api.max_retries, 1)
            while (retries := retries + 1) < _max_retries:
                if response.status_code != api.http_invalid_token_status:
                    api.last_token_injection = datetime.utcnow()
                    return response
                logs.warning(
                    {
                        "warning": f"Invalid token, refreshing it and retrying (retries: {retries})...",
                        "response.status_code": response.status_code,
                        "response.content": response.json(),
                    }
                )
                await refresh_access_api_token(api)
                async with httpx.AsyncClient(headers=api.auth_header) as client:
                    response = await f(*args, client=client, api=api, **kwargs)

            logs.error(
                {
                    "error": f"Max retries exceeded (retries: {_max_retries})",
                    "response.status_code": response.status_code,
                    "response.content": response.json(),
                }
            )
            raise InvalidStatusError(response)

        return wrapper

    return function_inject_tokens
