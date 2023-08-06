from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_custom_views(client: AsyncClient, api: Api, params: dict) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/custom_views"
    response = await client.get(url, params=params)
    return response
