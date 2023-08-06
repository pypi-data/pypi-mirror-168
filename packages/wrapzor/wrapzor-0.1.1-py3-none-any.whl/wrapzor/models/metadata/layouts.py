from datetime import datetime

from pydantic import BaseModel


class Section(BaseModel):
    id: str
    api_name: str
    display_label: str
    enable_colour_code: bool | None
    fields: list | None
    generate_type: str | None
    isSubformSection: bool
    name: str
    searchable: bool | None
    sequence_number: int
    show_business_card: bool | None
    source: str | None
    status: str | None
    type: str


class Profile(BaseModel):
    id: str
    default: bool
    name: str
    _default_view: dict


class Layout(BaseModel):
    id: str
    _default_view: dict | None
    actions_allowed: dict
    convert_mapping: dict | None
    created_by: dict | None
    created_for: dict | None
    created_time: datetime | None
    display_label: str
    generated_type: str
    has_more_profiles: bool
    modified_by: dict | None
    modified_time: datetime | None
    name: str
    profiles: list[Profile]
    sections: list[Section]
    show_business_card: bool
    source: str
    status: str
    visible: bool


class Layouts(BaseModel):
    layouts: list[Layout]


class LayoutsRequest(BaseModel):
    module: str

    class Config:
        use_enum_values = True
