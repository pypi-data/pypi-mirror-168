from httpx import AsyncClient, Response
from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_territories(client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/territories"
    response = await client.get(url)
    return response


@inject_tokens()
async def assign_territories(module: str, data: dict, client: AsyncClient, api: Api, record_id: str | None = None) -> Response:
    if record_id is None:
      url = f"{api.domain}/crm/{api.version}/{module}/actions/assign_territories"
    else:
      url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/actions/assign_territories"

    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def remove_territories(module: str, data: dict, client: AsyncClient, api: Api, record_id: str | None = None) -> Response:
    if record_id is None:
      url = f"{api.domain}/crm/{api.version}/{module}/actions/remove_territories"
    else:
      url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/actions/remove_territories"

    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def get_record_territories(module: str, record_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}"
    response = await client.get(url)
    return response