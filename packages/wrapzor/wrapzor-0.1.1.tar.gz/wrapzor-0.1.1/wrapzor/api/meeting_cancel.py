from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def cancel_meeting(event_id: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/Events/{event_id}/actions/cancel"
    response = await client.post(url, data=data)
    return response