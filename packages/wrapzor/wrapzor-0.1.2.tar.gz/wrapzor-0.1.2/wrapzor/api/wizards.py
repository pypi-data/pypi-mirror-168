from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_wizards(
    client: AsyncClient,
    api: Api,
    wizard_id: str | None = None,
    params: dict | None = None
) -> Response:
    if id is None:
        url = f"{api.domain}/crm/{api.version}/settings/wizards"
    else:
        url= f"{api.domain}/crm/{api.version}/settings/wizards/{wizard_id}"

    response = await client.get(url, params=params)
    return response
