from pydantic import BaseModel


class Field(BaseModel):
    id: str
    allowed_permissions_to_update: dict | None
    api_name: str
    association_details: str | None
    auto_number: dict
    businesscard_supported: bool
    created_source: str
    crypt: dict | None
    currency: dict
    custom_field: bool
    data_type: str
    decimal_place: int | None
    display_field: bool
    display_label: str
    display_type: int
    email_parser: dict
    enable_colour_code: bool
    external: str | None
    field_label: str
    field_read_only: bool
    filterable: bool
    formula: dict
    history_tracking: dict | None
    json_type: str
    length: int
    lookup: dict
    mass_update: bool
    multi_module_lookup: dict
    multiselectlookup: dict | None
    pick_list_values: list
    pick_list_values_sorted_lexically: bool
    profiles: list
    quick_sequence_number: str | None
    read_only: bool
    searchable: bool
    separator: bool
    sortable: bool
    subform: dict | None
    system_mandatory: bool
    tooltip: dict | None
    type: str
    ui_type: int
    unique: dict
    view_type: dict
    virtual_field: bool
    visible: bool
    webhook: bool


class Fields(BaseModel):
    fields: list[Field]


class FieldsRequest(BaseModel):
    module: str
    type: str | None = None  # unused
    include: str | None = None  # allowed_permissions_to_update

    class Config:
        use_enum_values = True
