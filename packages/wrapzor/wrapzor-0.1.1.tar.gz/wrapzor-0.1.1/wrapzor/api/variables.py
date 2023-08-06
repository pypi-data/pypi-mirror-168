from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_variables(client: AsyncClient, api: Api, variable_id: str | None = None, params: dict | None = None) -> Response:
    if variable_id is None:
        url = f"{api.domain}/crm/{api.version}/settings/variables"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/variables/{variable_id}"

    response = await client.get(url, params=params)
    return response


# variable_group = variable_group_id (or) variable_group_API_name
@inject_tokens()
async def get_variable_groups(variable_group: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/variable_groups/{variable_group}"

    response = await client.get(url)
    return response


@inject_tokens()
async def create_variables(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/variables"
    response = await client.post(url, data=data)
    return response


# variable_group = variable_group_id (or) variable_group_API_name
@inject_tokens()
async def update_variables(data: dict, client: AsyncClient, api: Api, variable_group: str | None = None) -> Response:
    if variable_group is None:
        url = f"{api.domain}/crm/{api.version}/settings/variables"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/variables/{variable_group}"

    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def delete_variables(client: AsyncClient, api: Api, variable_id: str | None = None, params: dict | None = None) -> Response:
    if variable_id is None:
        url = f"{api.domain}/crm/{api.version}/settings/variables"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/variables/{variable_id}"

    response = await client.delete(url, params=params)
    return response
