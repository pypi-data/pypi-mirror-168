from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_related_records(module: str, record_id: str, related_module: str, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/{related_module}"
    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def update_related_records(module: str, record_id: str, related_module: str, related_record_id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/{related_module}/{related_record_id}"
    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def delete_related_records(module: str, external_value: str, related_module: str, client: AsyncClient, api: Api, related_record_id: str | None = None, params: dict | None = None) -> Response:
    if related_record_id is None:
        url = f"{api.domain}/crm/{api.version}/{module}/{external_value}/{related_module}"
    else:
        url = f"{api.domain}/crm/{api.version}/{module}/{external_value}/{related_module}/{related_record_id}"

    response = await client.delete(url, params=params)
    return response
