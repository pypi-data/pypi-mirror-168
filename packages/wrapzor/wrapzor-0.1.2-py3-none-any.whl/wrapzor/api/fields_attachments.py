from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def download_fields_attachments(
    module: str,
    record_id: str,
    client: AsyncClient,
    api: Api,
    params: dict | None = None
) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/actions/download_fields_attachment"

    response = await client.get(url, params=params)
    return response
