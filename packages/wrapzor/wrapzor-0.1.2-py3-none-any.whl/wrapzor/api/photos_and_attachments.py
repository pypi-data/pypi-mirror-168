from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_attachments(module: str, record_id: str, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/Attachments"
    response = await client.get(url, params=params)
    return response


# content type as multipart/form data
@inject_tokens()
async def upload_attachment(module: str, record_id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/Attachments"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def download_attachment(module: str, record_id: str, attachment_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/Attachments/{attachment_id}"
    response = await client.get(url)
    return response


@inject_tokens()
async def delete_attachment(module: str, record_id: str, attachment_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/Attachments/{attachment_id}"
    response = await client.delete(url)
    return response


# content type as multipart/form data
@inject_tokens()
async def upload_photo(module: str, record_id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/photo"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def download_photo(module: str, record_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/photo"
    response = await client.get(url)
    return response


@inject_tokens()
async def delete_photo(module: str, record_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/photo"
    response = await client.delete(url)
    return response
