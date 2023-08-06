import os
from pathlib import Path

ZOHO_CLIENT_ID = os.environ["ZOHO_CLIENT_ID"]
ZOHO_CLIENT_PASSWORD = os.environ["ZOHO_CLIENT_PASSWORD"]
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_CODE = os.getenv("ZOHO_CODE")
ZOHO_ACCOUNT_DOMAIN = os.getenv("ZOHO_ACCOUNT_DOMAIN", "https://accounts.zoho.eu")
CURRENT_DIR = Path(__file__).parent
STATIC_DIR = CURRENT_DIR / "static"