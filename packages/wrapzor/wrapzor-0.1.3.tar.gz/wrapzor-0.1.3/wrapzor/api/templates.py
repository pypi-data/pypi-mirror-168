from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_email_templates(client: AsyncClient, api: Api, id: str | None = None, params: dict | None = None) -> Response:
    if id is None:
        url = f"{api.domain}/crm/{api.version}/settings/email_templates"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/email_templates/{id}"

    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def get_inventory_templates(client: AsyncClient, api: Api, id: str | None = None, params: dict | None = None) -> Response:
    if id is None:
        url = f"{api.domain}/crm/{api.version}/settings/inventory_templates"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/inventory_templates/{id}"

    response = await client.get(url, params=params)
    return response
