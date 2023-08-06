from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api

# Header
# X-EXTERNAL: {module_API_name}.{external_field_API_name}


@inject_tokens()
async def get_related_records_using_external_id(module: str, external_value: str, related_module: str, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{external_value}/{related_module}"
    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def update_related_records_using_external_id(module: str, external_value: str, related_module: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{external_value}/{related_module}"
    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def delete_related_records_using_external_id(module: str, external_value: str, related_module: str, related_external_value: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{external_value}/{related_module}/{related_external_value}"
    response = await client.delete(url)
    return response
