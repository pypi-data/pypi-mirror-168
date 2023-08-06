from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_roles(client: AsyncClient, api: Api, role_id: str | None = None) -> Response:
    if role_id is None:
        url = f"{api.domain}/crm/{api.version}/settings/roles"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/roles/{role_id}"

    response = await client.get(url)
    return response


@inject_tokens()
async def create_roles(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/roles"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def update_roles(
    data: dict,
    client: AsyncClient,
    api: Api,
    role_id: str | None = None
) -> Response:
    if role_id is None:
        url = f"{api.domain}/crm/{api.version}/settings/roles"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/roles/{role_id}"

    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def delete_role(
    role_id: str,
    params: dict,
    client: AsyncClient,
    api: Api,
) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/roles/{role_id}"
    response = await client.delete(url, params=params)
    return response
