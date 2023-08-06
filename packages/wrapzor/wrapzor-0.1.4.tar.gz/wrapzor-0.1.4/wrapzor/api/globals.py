from wrapzor.api.modules import get_modules, get_api_map_names

MODULES = await get_modules()
API_MAP_NAMES = get_api_map_names(MODULES)
