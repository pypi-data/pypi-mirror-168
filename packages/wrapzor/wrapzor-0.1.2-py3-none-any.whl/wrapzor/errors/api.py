from enum import Enum

from httpx import Response


class InvalidStatusError(Exception):
    def __int__(self, response: Response):
        self.response = response


class ArgsError(Exception):
    def __int__(self, response: Response):
        self.response = response


class TimeOut(Exception):
    def __int__(self, response: Response):
        self.response = response


class Message(str, Enum):
    missing_domain = (
        "Please verify your API configuration: the domain -URL- and the account domain -URL- must exist and start by "
        "http (check ZOHO_DOMAIN in the .env) "
    )
    bad_domain = "Please verify your domain, it must start by http"
    missing_api_version = (
        "Please verify your API configuration: you need to set the ZOHO_API_VERSION in your "
        ".env "
    )
    suffix_mismatch = "Top Level Domain (.com/.eu/.fr) mismatch between account domain and api domain."
    env_mismatch = (
        "If you set ZOHO_CODE and ZOHO_REFRESH_CODE in your env then the first will be used to fetch a new "
        "REFRESH_TOKEN and ZOH_REFRESH_TOKEN won't be used "
    )
    input_data_missing = (
        "Input model has been set to verify data but neither data nor params has been filled as "
        "arguments "
    )
