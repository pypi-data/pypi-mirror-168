from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def create_user(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/users"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def get_users(
    client: AsyncClient, api: Api, params: dict | None = None, user_id: str | None = None
) -> Response:
    if user_id is None:
        url = f"{api.domain}/crm/{api.version}/users"
    else:
        url = f"{api.domain}/crm/{api.version}/users/{user_id}"

    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def update_user(
    data: dict,
    client: AsyncClient,
    api: Api,
    user_id: str | None = None
) -> Response:
    if user_id is None:
        url = f"{api.domain}/crm/{api.version}/users"
    else:
        url = f"{api.domain}/crm/{api.version}/users/{user_id}"

    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def delete_user(
    user_id: str,
    client: AsyncClient,
    api: Api,
) -> Response:
    url = f"{api.domain}/crm/{api.version}/users/{user_id}"
    response = await client.delete(url)
    return response


@inject_tokens()
async def get_user_territories(
    user_id: str, client: AsyncClient, api: Api, territory_id: str | None = None, params: dict | None = None
) -> Response:
    if territory_id is None:
        url = f"{api.domain}/crm/{api.version}/users/{user_id}/territories"
    else:
        url = f"{api.domain}/crm/{api.version}/users/{user_id}/territories/{territory_id}"

    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def add_user_territories(
    user_id: str,
    data: dict,
    client: AsyncClient,
    api: Api,
) -> Response:
    url = f"{api.domain}/crm/{api.version}/users/{user_id}/territories"
    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def get_user_territories_validate_before_transfer(
    user_id: str, client: AsyncClient, api: Api, territory_id: str | None = None
) -> Response:
    if territory_id is None:
        url = f"{api.domain}/crm/{api.version}/users/{user_id}/territories/actions/validate_before_transfer"
    else:
        url = f"{api.domain}/crm/{api.version}/users/{user_id}/territories/{territory_id}/actions/validate_before_transfer"

    response = await client.get(url)
    return response


@inject_tokens()
async def user_transfer_and_delink_territories(
    user_id: str, data: dict, client: AsyncClient, api: Api,, territory_id: str | None = None
) -> Response:
    if territory_id is None:
        url = f"{api.domain}/crm/{api.version}/users/{user_id}/territories/actions/transfer_and_delink"
    else:
        url = f"{api.domain}/crm/{api.version}/users/{user_id}/territories/{territory_id}/actions/transfer_and_delink"

    response = await client.put(url, data=data)
    return response
