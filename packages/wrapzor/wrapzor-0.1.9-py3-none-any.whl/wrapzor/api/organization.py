from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_organization(client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/org"
    response = await client.get(url)
    return response

@inject_tokens()
async def upload_organization_photo(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/org/photo"
    response = await client.post(url, data=data)
    return response
