from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_scoring_rules(client: AsyncClient, api: Api, rule_id: str | None = None, params: dict | None = None) -> Response:
    if rule_id is None:
        url = f"{api.domain}/crm/{api.version}/settings/automation/scoring_rules"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/automation/scoring_rules/{rule_id}"

    response = await client.get(url, params=params)
    return response


@inject_tokens()
async def create_scoring_rules(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/automation/scoring_rules"
    response = await client.post(url, data=data)
    return response


@inject_tokens()
async def update_scoring_rules(data: dict, client: AsyncClient, api: Api, rule_id: str | None = None) -> Response:
    if rule_id is None:
        url = f"{api.domain}/crm/{api.version}/settings/automation/scoring_rules"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/automation/scoring_rules/{rule_id}"

    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def execute_scoring_rules(module: str, data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/actions/run_scoring_rules"

    response = await client.put(url, data=data)
    return response


@inject_tokens()
async def delete_scoring_rules(client: AsyncClient, api: Api, rule_id: str | None = None, params: dict | None = None) -> Response:
    if rule_id is None:
        url = f"{api.domain}/crm/{api.version}/settings/automation/scoring_rules"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/automation/scoring_rules/{rule_id}"

    response = await client.delete(url, params=params)
    return response


@inject_tokens()
async def activate_scoring_rule_status(rule_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/automation/scoring_rules/{rule_id}/actions/activate"

    response = await client.put(url)
    return response


@inject_tokens()
async def deactivate_scoring_rule_status(rule_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/automation/scoring_rules/{rule_id}/actions/activate"

    response = await client.delete(url)
    return response


@inject_tokens()
async def cloning_scoring_rule(rule_id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/automation/scoring_rules/{rule_id}/actions/clone"
    response = await client.post(url)
    return response


@inject_tokens()
async def get_entity_score(module: str, record_id: str, params: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/{api.version}/{module}/{record_id}/Entity_Scores__s"

    response = await client.get(url, params=params)
    return response
