from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


# content type as multipart/form data
@inject_tokens()
async def upload_files(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/files"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def get_files(client: AsyncClient, api: Api, params: dict) -> Response:
    url = f"{api.domain}/crm/{api.version}/files"
    response = await client.get(url, params=params)
    return response
