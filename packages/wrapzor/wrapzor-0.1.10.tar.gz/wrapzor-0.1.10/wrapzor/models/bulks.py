from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Creator(BaseModel):
    id: str
    name: str


class Details(BaseModel):
    id: str
    operation: str
    state: str
    created_by: Creator
    created_time: datetime


class BulkDataResponse(BaseModel):
    status: str
    code: str
    message: str
    details: Details


class BulkResponse(BaseModel):
    data: list[BulkDataResponse]
    info: dict


class Result(BaseModel):
    page: int
    per_page: int
    count: int
    download_url: str
    more_records: bool


class Module(BaseModel):
    id: str
    api_name: str


class Query(BaseModel):
    module: Module
    page: int


class BulkDataStatusResponse(BaseModel):
    id: str
    operation: str
    state: str
    result: Result | None = None
    query: Query
    created_by: Creator
    created_time: datetime
    file_type: Literal["csv", "ics"]


class BulkStatusResponse(BaseModel):
    data: list[BulkDataStatusResponse]
