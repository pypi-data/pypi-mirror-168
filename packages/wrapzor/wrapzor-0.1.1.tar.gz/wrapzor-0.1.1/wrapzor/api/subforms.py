from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_record_subforms(module: str, record_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}"
    response = await client.get(url)
    return response


@inject_tokens()
async def get_subforms(subform: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{subform}"
    response = await client.get(url)
    return response


@inject_tokens()
async def create_subforms(module: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def update_subforms(module: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}"
    response = await client.put(url, data=data)
    return response