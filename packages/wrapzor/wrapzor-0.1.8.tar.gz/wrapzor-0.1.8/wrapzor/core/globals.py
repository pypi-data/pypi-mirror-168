from wrapzor.env import ZOHO_CODE, ZOHO_CLIENT_ID, ZOHO_CLIENT_PASSWORD, ZOHO_ACCOUNT_DOMAIN, ZOHO_REFRESH_TOKEN
from wrapzor.core.api import Api


API = Api(
    code=ZOHO_CODE,
    client_id=ZOHO_CLIENT_ID,
    client_secret=ZOHO_CLIENT_PASSWORD,
    account_domain=ZOHO_ACCOUNT_DOMAIN,
    _refresh_token=ZOHO_REFRESH_TOKEN,
)
