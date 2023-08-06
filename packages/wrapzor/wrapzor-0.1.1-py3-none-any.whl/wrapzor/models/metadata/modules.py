from datetime import datetime

from pydantic import BaseModel, AnyUrl


class Module(BaseModel):
    id: str
    # "$field_states": list
    # "$on_demand_properties": list
    # "$properties": list
    api_name: str
    api_supported: bool
    arguments: list
    business_card_field_limit: int
    convertable: bool
    creatable: bool
    custom_view: dict
    deletable: bool
    description: str | None
    display_field: str
    editable: bool
    emailTemplate_support: bool
    email_parser_supported: bool
    feeds_required: bool
    filter_status: bool
    filter_supported: bool
    generated_type: str
    global_search_supported: bool
    inventory_template_supported: bool
    isBlueprintSupported: bool
    kanban_view: bool
    kanban_view_supported: bool
    lookup_field_properties: dict | None
    modified_by: dict | None
    modified_time: datetime | None
    module_name: str
    parent_module: dict
    per_page: int
    plural_label: str
    presence_sub_menu: bool
    profiles: list
    quick_create: bool
    related_list_properties: dict
    scoring_supported: bool
    search_layout_fields: list
    sequence_number: int
    show_as_tab: bool
    singular_label: str
    territory: dict | None
    triggers_supported: bool
    viewable: bool
    visibility: int
    visible: bool
    web_link: AnyUrl | None
    webform_supported: bool


class Modules(BaseModel):
    modules: list[Module]
