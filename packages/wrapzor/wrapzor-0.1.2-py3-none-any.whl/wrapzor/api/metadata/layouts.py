from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api
from wrapzor.core.verify import verify_data
from wrapzor.models.metadata.layouts import Layouts, LayoutsRequest


@verify_data(input_model=LayoutsRequest, output_model=Layouts)
@inject_tokens()
async def get_layouts(client: AsyncClient, api: Api, params: dict) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/layouts"
    response = await client.get(url, params=params)
    return response
