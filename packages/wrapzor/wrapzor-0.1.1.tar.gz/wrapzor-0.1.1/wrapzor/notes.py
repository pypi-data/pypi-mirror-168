from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_notes(params: dict, client: AsyncClient, api: Api, note_id: str | None = None) -> Response:
    if note_id is None:
        url = f"{api.domain}/crm/{api.version}/Notes"
    else:
        url = f"{api.domain}/crm/{api.version}/Notes/{note_id}"

    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def get_record_notes(module: str, record_id: str, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/Notes"

    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def create_notes(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/Notes"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def create_record_notes(module: str, record_id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/Notes"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def update_notes(data: dict, client: AsyncClient, api: Api, note_id: str | None = None) -> Response:
    if note_id is None:
        url = f"{api.domain}/crm/{api.version}/Notes"
    else:
        url = f"{api.domain}/crm/{api.version}/Notes/{note_id}"

    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def update_record_notes(module: str, record_id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/Notes"
    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def delete_notes(client: AsyncClient, api: Api, note_id: str | None = None, params: dict | None = None) -> Response:
    if note_id is None:
        url = f"{api.domain}/crm/{api.version}/Notes"
    else:
        url = f"{api.domain}/crm/{api.version}/Notes/{note_id}"

    response = await client.delete(url, params=params)
    return response


@inject_tokens()
async def delete_record_note(module: str, record_id: str, note_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/Notes/{note_id}"
    response = await client.delete(url)
    return response
