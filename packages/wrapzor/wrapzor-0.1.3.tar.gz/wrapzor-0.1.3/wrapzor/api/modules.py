from httpx import AsyncClient, Response

from wrapzor.core.tokens import inject_tokens, Api
from wrapzor.core.verify import verify_data
from wrapzor.models.modules import Modules, Module


@verify_data(output_model=Modules)
@inject_tokens()
async def get_modules(client: AsyncClient, api: Api) -> Response | Modules:
    url = f"{api.domain}/crm/{api.version}/settings/modules"
    response = await client.get(url)
    return response


@verify_data(output_model=Modules)
@inject_tokens()
async def get_module(module: str, client: AsyncClient, api: Api) -> Response | Module:
    url = f"{api.domain}/crm/{api.version}/settings/modules/{module}"
    response = await client.get(url)
    return response


def get_api_map_names(modules: Modules) -> dict[str, str]:
    api_supported_modules = list(
        filter(lambda module: module.api_supported, modules.modules)
    )
    return {module.module_name: module.api_name for module in api_supported_modules}
