from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_users_unavailability(
    client: AsyncClient,
    api: Api,
    id: str | None = None,
    params: dict | None = None
) -> Response:
    if id is None:
        url = f"{api.domain}/crm/{api.version}/settings/users_unavailability"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/users_unavailability/{id}"

    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def create_users_unavailability(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/users_unavailability"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def update_users_unavailability(
    data: dict,
    client: AsyncClient,
    api: Api,
    id: str | None = None
) -> Response:
    if id is None:
        url = f"{api.domain}/crm/{api.version}/settings/users_unavailability"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/users_unavailability/{id}"

    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def delete_users_unavailability(
    id: str,
    client: AsyncClient,
    api: Api,
) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/users_unavailability/{id}"
    response = await client.delete(url)
    return response
