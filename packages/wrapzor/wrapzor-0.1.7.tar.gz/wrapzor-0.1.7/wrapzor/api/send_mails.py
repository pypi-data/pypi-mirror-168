from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_from_addresses(client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/emails/actions/from_addresses"
    response = await client.get(url)
    return response


@inject_tokens()
async def send_mail(module: str, record_id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/actions/send_mail"
    response = await client.post(url, data=data)
    return response

# {api - domain} / crm / {version} / {module_api_name} / {record_id} / actions / send_mail
