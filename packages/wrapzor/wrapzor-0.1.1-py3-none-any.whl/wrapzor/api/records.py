from httpx import AsyncClient, Response
from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_records(module: str, params: dict, client: AsyncClient, api: Api, record_id: str | None = None) -> Response:
    if record_id is None:
        url = f"{api.domain}/crm/{api.version}/{module}"
    else:
        url = f"{api.domain}/crm/{api.version}/{module}/{record_id}"
    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def create_records(module: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def update_records(
    module: str,
    data: dict,
    client: AsyncClient,
    api: Api,
) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}"
    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def upsert_records(module: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/upsert"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def delete_records(
    module: str,
    params: dict,
    client: AsyncClient,
    api: Api,
) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}"
    response = await client.delete(url, params=params)
    return response


@inject_tokens()
async def get_lead_conversion_options(id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/Leads/{id}/__conversion_options"
    response = await client.get(url)
    return response


@inject_tokens()
async def convert_lead(id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/Leads/{id}/actions/convert"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def get_deleted_records(module: str, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/deleted"
    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def search_records(module: str, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/search"
    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def get_record_count(module: str, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/actions/count"
    response = await client.get(url, params=params)
    return response
