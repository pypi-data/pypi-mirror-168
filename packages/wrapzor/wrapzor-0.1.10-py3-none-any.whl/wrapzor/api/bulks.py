from asyncio import sleep
from pathlib import Path

from httpx import AsyncClient, Response

from wrapzor.api.utils import get_job_state, get_job_id
from wrapzor.core.tokens import inject_tokens, Api
from wrapzor.errors.api import TimeOut
from wrapzor.logs import logs
from wrapzor.utils import now_str
from wrapzor.env import STATIC_DIR

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
    filename:str, id: str, client: AsyncClient, api: Api, path: str | Path | None = None, filename_only: bool = False
) -> Response:
    if path is None:
        path = STATIC_DIR / "bulks"
    print(path)
    path = Path(path) if isinstance(path, str) else path
    url = f"{api.domain}/crm/bulk/{api.version}/read/{id}/result"
    response = await client.get(url=url)
    final_path = path / f"{filename}.zip" if filename_only else path / f"{filename}___{id}_{now_str()}.zip"
    with open(final_path, "wb") as file:
        file.write(response.content)
    return response


async def get_bulk(filename: str, data: dict, path: str | Path | None = None, filename_only: bool = False):
    res_creation = await create_bulk(data=data)
    job_id = get_job_id(res_creation)
    await wait_for_job_done(id=job_id)
    await download_bulk_result(filename= filename, id=job_id, path=path, filename_only=filename_only)
    return filename