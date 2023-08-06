from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_tags(params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/tags"
    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def add_tags_to_records(module: str, data: dict, client: AsyncClient, api: Api, record_id: str | None = None) -> Response:
    if record_id is None:
        url = f"{api.domain}/crm/{api.version}/{module}/settings/add_tags"
    else:
        url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/settings/add_tags"

    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def remove_tags_to_records(module: str, data: dict, client: AsyncClient, api: Api, record_id: str | None = None) -> Response:
    if record_id is None:
        url = f"{api.domain}/crm/{api.version}/{module}/settings/remove_tags"
    else:
        url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/settings/remove_tags"

    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def create_tags(params: dict, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/tags"
    response = await client.post(url, data=data, params=params)
    return response


@inject_tokens()
async def update_tags(params: dict, data: dict, client: AsyncClient, api: Api, tag_id: str | None = None) -> Response:
    if tag_id is None:
        url = f"{api.domain}/crm/{api.version}/settings/tags"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/tags/{tag_id}"

    response = await client.put(url, data=data, params=params)
    return response


@inject_tokens()
async def get_tag_records_count(tag_id: str, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/tags/{tag_id}/actions/records_count"
    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def merge_tags(tag_id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/tags/{tag_id}/actions/merge"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def delete_tag(tag_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/tags/{tag_id}"
    response = await client.delete(url)
    return response
