from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_pipelines(client: AsyncClient, api: Api, params: dict, pipeline_id: str | None = None) -> Response:
    if pipeline_id is None:
        url = f"{api.domain}/crm/{api.version}/settings/pipeline"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/pipeline/{pipeline_id}"

    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def create_pipeline(data: dict, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/pipeline"
    response = await client.post(url, data=data, params=params)
    return response


@inject_tokens()
async def update_pipeline(
    data: dict,
    params: dict,
    pipeline_id: str,
    client: AsyncClient,
    api: Api,
) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/pipeline/{pipeline_id}"
    response = await client.put(url, data=data, params=params)
    return response


@inject_tokens()
async def transfer_and_delete_pipeline(
    data: dict,
    params: dict,
    client: AsyncClient,
    api: Api,
) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/pipeline/actions/transfer"
    response = await client.post(url, data=data, params=params)
    return response
