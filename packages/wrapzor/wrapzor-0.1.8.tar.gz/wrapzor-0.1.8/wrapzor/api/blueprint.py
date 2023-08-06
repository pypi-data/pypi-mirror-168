from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_blueprint(module: str, record_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/actions/blueprint"

    response = await client.get(url)
    return response


@inject_tokens()
async def update_blueprint(module: str, record_id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/actions/blueprint"

    response = await client.put(url, data=data)
    return response
