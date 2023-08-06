from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def share_records(module: str, record_id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/actions/share"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def get_shared_records(module: str, record_id: str, client: AsyncClient, api: Api, params: dict | None = None) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/actions/share"
    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def update_share_permissions(
    module: str,
    record_id: str,
    data: dict,
    client: AsyncClient,
    api: Api,
) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/actions/share"
    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def revoke_shared_records(
    module: str,
    record_id: str,
    client: AsyncClient,
    api: Api,
) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/actions/share"
    response = await client.delete(url)
    return response
