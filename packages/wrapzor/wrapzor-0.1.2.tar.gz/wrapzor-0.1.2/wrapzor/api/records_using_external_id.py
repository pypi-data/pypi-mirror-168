from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api

# Header
# X-EXTERNAL: {module_API_name}.{external_field_API_name}


@inject_tokens()
async def get_records_using_external_id(module: str, external_value: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{external_value}"
    response = await client.get(url)
    return response


@inject_tokens()
async def create_records_using_external_id(module: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def update_records_using_external_id(module: str, external_value: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{external_value}"
    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def delete_records_using_external_id(module: str, client: AsyncClient, api: Api, external_value: str | None = None, params: dict | None = None) -> Response:
    if external_value is None:
        url = f"{api.domain}/crm/{api.version}/{module}"
    else:
        url = f"{api.domain}/crm/{api.version}/{module}/{external_value}"

    response = await client.delete(url, params=params)
    return response


@inject_tokens()
async def upsert_records_using_external_id(module: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/upsert"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def search_records(module: str, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/search"
    response = await client.get(url, params=params)
    return response
