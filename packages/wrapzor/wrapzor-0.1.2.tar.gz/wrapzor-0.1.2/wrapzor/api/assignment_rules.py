from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api


@inject_tokens()
async def get_assignment_rules(client: AsyncClient, api: Api, params: dict | None = None, rule_id: str | None = None) -> Response:
    if rule_id is None:
        url = f"{api.domain}/crm/{api.version}/settings/automation/assignment_rules"
    else:
        url = f"{api.domain}/crm/{api.version}/settings/automation/assignment_rules/{rule_id}"

    response = await client.get(url, params=params)
    return response
