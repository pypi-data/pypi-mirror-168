from httpx import AsyncClient, Response

from src.core.tokens import inject_tokens, Api
from src.core.verify import verify_data
from src.models.metadata.fields import Fields, FieldsRequest


@verify_data(input_model=FieldsRequest, output_model=Fields)
@inject_tokens()
async def get_fields(client: AsyncClient, api: Api, params: dict) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/fields"
    response = await client.get(url, params=params)
    return response
