from env import *
from src.core.api import Api


API = Api(
    code=ZOHO_CODE,
    client_id=ZOHO_CLIENT_ID,
    client_secret=ZOHO_CLIENT_PASSWORD,
    account_domain=ZOHO_ACCOUNT_DOMAIN,
    _refresh_token=ZOHO_REFRESH_TOKEN,
)
