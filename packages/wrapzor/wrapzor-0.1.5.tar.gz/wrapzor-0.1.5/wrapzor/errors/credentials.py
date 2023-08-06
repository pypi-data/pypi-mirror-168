from enum import Enum


class Message(str, Enum):
    missing_client_id = "Please verify your credentials: you need to set ZOHO_CLIENT_ID"
    missing_code = (
        "Please verify your credentials: you need to set ZOHO_CODE, please check the "
        "README to see where to find this code. "
    )
    missing_client_secret = "Please verify your credentials: you need to set ZOHO_CLIENT_PASSWORD in your .env"
    too_small_code = "Please verify your ZOHO_CODE it seems small"
    too_small_client_id = "Please verify your ZOHO_CLIENT_ID it seems small"
    too_small_client_secret = "Please verify your ZOHO_CLIENT_PASSWORD it seems small"
