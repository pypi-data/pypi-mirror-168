from datetime import datetime

from pydantic import BaseModel, AnyUrl


class Module(BaseModel):
    id: str
    api_name: str
    api_supported: bool
    arguments: list
    business_card_field_limit: int
    convertable: bool
    creatable: bool
    custom_view: dict | None
    deletable: bool
    description: str | None
    editable: bool
    emailTemplate_support: bool
    email_parser_supported: bool
    feeds_required: bool
    filter_supported: bool
    generated_type: str
    global_search_supported: bool
    inventory_template_supported: bool
    isBlueprintSupported: bool
    modified_by: dict | None
    modified_time: datetime | None
    module_name: str
    parent_module: dict
    plural_label: str
    presence_sub_menu: bool
    profiles: list
    quick_create: bool
    scoring_supported: bool
    sequence_number: int | None
    show_as_tab: bool
    singular_label: str
    triggers_supported: bool
    viewable: bool
    visibility: int
    visible: bool
    web_link: AnyUrl | None
    webform_supported: bool


class Modules(BaseModel):
    modules: list[Module]
