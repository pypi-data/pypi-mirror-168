from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api
from wrapzor.core.verify import verify_data
from wrapzor.models.metadata.fields import Fields, FieldsRequest


@verify_data(input_model=FieldsRequest, output_model=Fields)
@inject_tokens()
async def get_fields(client: AsyncClient, api: Api, params: dict) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/fields"
    response = await client.get(url, params=params)
    return response
