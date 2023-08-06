from pydantic import BaseModel


class Id(BaseModel):
    id: str


class PostResponse(BaseModel):
    code: str
    details: Id
    message: str
    status: str


class PaginationRequest(BaseModel):
    page: int | None = 1
    per_page: int | None = 200


class PaginationResponse(BaseModel):
    per_page: int
    count: int
    page: int
    more_records: bool
