from datetime import datetime

from pydantic import BaseModel
from wrapzor.models.generics import PaginationResponse


class CustomViewsPaginationResponse(PaginationResponse):
    default: str
    translation: dict


class CustomView(BaseModel):
    id: str
    category: str
    created_by: dict | None
    created_time: datetime | None
    default: bool
    display_value: str
    favorite: int | None
    last_accessed_time: datetime | None
    locked: bool
    modified_by: dict | None
    modified_time: datetime | None
    name: str
    system_defined: bool
    system_name: str | None


class CustomViews(BaseModel):
    custom_views: list[CustomView]
    info: CustomViewsPaginationResponse


class CustomViewsRequest(BaseModel):
    module: str

    class Config:
        use_enum_values = True
