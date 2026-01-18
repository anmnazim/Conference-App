import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_drive_service():
    creds_info = json.loads(os.environ["GOOGLE_DRIVE_CREDENTIALS"])

    credentials = service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=SCOPES
    )

    return build("drive", "v3", credentials=credentials)
