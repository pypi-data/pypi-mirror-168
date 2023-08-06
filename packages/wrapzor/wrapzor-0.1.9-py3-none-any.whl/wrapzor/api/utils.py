from httpx import Response

from wrapzor.models.bulks import BulkResponse, BulkStatusResponse


def get_keys_and_types(response: Response):
    result = {}
    res_json = response.json()
    for key in res_json:
        sub_result = {}
        if isinstance(res_json[key], list):
            data = res_json[key][0]
            for _ in data:
                sub_result[_] = type(data[_])
            result[key] = sub_result
        else:
            result[key] = res_json[key]
    return result


def get_job_id(response: Response | BulkResponse) -> str:
    res = (
        BulkResponse(**response.json()) if isinstance(response, Response) else response
    )
    return res.data[0].details.id


def get_job_state(response: Response | BulkStatusResponse) -> str:
    res = (
        BulkStatusResponse(**response.json())
        if isinstance(response, Response)
        else response
    )
    return res.data[0].state
