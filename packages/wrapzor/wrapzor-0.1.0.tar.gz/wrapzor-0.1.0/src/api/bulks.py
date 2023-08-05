from asyncio import sleep
from pathlib import Path

from httpx import AsyncClient, Response

from src.api.utils import get_job_state, get_job_id
from src.core.tokens import inject_tokens, Api
from errors import TimeOut
from src.logs import logs
from src.utils import now_str

COMPLETED = "COMPLETED"
HOUR = 60 * 60


@inject_tokens()
async def create_bulk(data: dict, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/bulk/{api.version}/read"
    response = await client.post(url=url, data=data)
    return response


@inject_tokens()
async def get_bulk_status(id: str, client: AsyncClient, api: Api) -> Response:
    url = f"{api.domain}/crm/bulk/v3/read/{id}"
    response = await client.get(url=url)
    return response


async def wait_for_job_done(id: str, seconds: int = 5, max_wait=HOUR):
    slept = 0
    while True:
        response = await get_bulk_status(id)
        print(response.status_code)
        print(response.json())

        state = get_job_state(response)
        logs.debug(f"Fetching job progress: {state}")
        if slept >= max_wait:
            raise TimeOut(response)
        if state == COMPLETED:
            break
        await sleep(seconds)
        slept += seconds
    return response


@inject_tokens()
async def download_bulk_result(
    id: str, client: AsyncClient, api: Api, path: str | Path | None = None
) -> Response:
    if path is None:
        path = Path("static/downloads")
    print(path)
    path = Path(path) if isinstance(path, str) else path
    url = f"{api.domain}/crm/bulk/{api.version}/read/{id}/result"
    response = await client.get(url=url)
    with open(path / f"{id}_{now_str()}.zip", "wb") as file:
        file.write(response.content)
    return response


async def get_bulk(data: dict, path: str | Path | None = None):
    res_creation = await create_bulk(data=data)
    job_id = get_job_id(res_creation)
    await wait_for_job_done(id=job_id)
    await download_bulk_result(id=job_id, path=path)
