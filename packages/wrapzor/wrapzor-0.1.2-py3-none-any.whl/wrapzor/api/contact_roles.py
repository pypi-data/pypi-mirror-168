from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_contact_roles(client: AsyncClient, api: Api, contact_role_id: str | None = None) -> Response:
    if contact_role_id is None:
        url = f"{api.domain}/crm/{api.version}/Contacts/roles"
    else:
        url = f"{api.domain}/crm/{api.version}/Contacts/roles/{contact_role_id}"

    response = await client.get(url)
    return response


@inject_tokens()
async def create_contact_roles(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/Contacts/roles"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def update_contact_roles(data: dict, client: AsyncClient, api: Api, contact_role_id: str | None = None) -> Response:
    if contact_role_id is None:
        url = f"{api.domain}/crm/{api.version}/Contacts/roles"
    else:
        url = f"{api.domain}/crm/{api.version}/Contacts/roles/{contact_role_id}"

    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def delete_contact_roles(client: AsyncClient, api: Api, contact_role_id: str | None = None, params: dict | None = None) -> Response:
    if contact_role_id is None:
        url = f"{api.domain}/crm/{api.version}/Contacts/roles"
    else:
        url = f"{api.domain}/crm/{api.version}/Contacts/roles/{contact_role_id}"

    response = await client.delete(url, params=params)
    return response


@inject_tokens()
async def get_deal_contact_roles(deal_id: str, client: AsyncClient, api: Api, contact_id: str | None = None) -> Response:
    if contact_id is None:
        url = f"{api.domain}/crm/{api.version}/Deals/{deal_id}/Contact_Roles"
    else:
        url = f"{api.domain}/crm/{api.version}/Deals/{deal_id}/Contact_Roles/{contact_id}"

    response = await client.get(url)
    return response


@inject_tokens()
async def create_deal_contact_role(deal_id: str, contact_id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/Deals/{deal_id}/Contact_Roles/{contact_id}"
    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def delete_deal_contact_role(deal_id: str, contact_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/Deals/{deal_id}/Contact_Roles/{contact_id}"
    response = await client.delete(url)
    return response
