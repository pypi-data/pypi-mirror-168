from httpx import AsyncClient, Response
from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def change_owner(module: str, data: dict, client: AsyncClient, api: Api, record_id: str | None = None) -> Response:
    if record_id is None:
        url = f"{api.domain}/crm/{api.version}/{module}/actions/change_owner"
    else:
        url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/actions/change_owner"

    response = await client.post(url, data=data)
    return response
