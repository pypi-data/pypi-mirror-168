from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_mass_update_status(module: str, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/actions/mass_updates"
    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def mass_update_records(module: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/actions/mass_update"
    response = await client.post(url, data=data)
    return response
