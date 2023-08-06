from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_profiles(client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/profiles"
    response = await client.get(url)
    return response
