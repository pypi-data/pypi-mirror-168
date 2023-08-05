from pydantic import BaseModel


class RelatedList(BaseModel):
    id: str
    action: str | None
    api_name: str
    connectedmodule: str | None
    customize_display_label: bool
    customize_fields: bool
    customize_sort: bool
    display_label: str
    href: str | None
    linkingmodule: str | None
    module: dict | None
    name: str
    sequence_number: int
    type: str


class RelatedLists(BaseModel):
    related_lists: list[RelatedList]


class RelatedListsRequest(BaseModel):
    module: str
    layout_id: str | None = None

    class Config:
        use_enum_values = True
