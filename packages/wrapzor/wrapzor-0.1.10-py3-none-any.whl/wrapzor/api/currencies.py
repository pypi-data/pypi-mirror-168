from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def enable_multiple_currencies(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/org/currencies/actions/enable"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def get_currencies(client: AsyncClient, api: Api, currency_id: str | None = None) -> Response:
    if currency_id is None:
        url = f"{api.domain}/crm/{api.version}/org/currencies"
    else:
        url = f"{api.domain}/crm/{api.version}/org/currencies/{currency_id}"

    response = await client.get(url)
    return response


@inject_tokens()
async def create_currencies(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/org/currencies"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def update_currencies(
    data: dict,
    client: AsyncClient,
    api: Api,
    currency_id: str | None = None
) -> Response:
    if currency_id is None:
        url = f"{api.domain}/crm/{api.version}/org/currencies"
    elif currency_id == "home":
        url = f"{api.domain}/crm/{api.version}/org/currencies/actions/enable"
    else:
        url = f"{api.domain}/crm/{api.version}/org/currencies/{currency_id}"

    response = await client.put(url, data=data)
    return response
