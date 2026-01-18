import json
import os
import firebase_admin
from firebase_admin import credentials, storage

def init_firebase():
    if not firebase_admin._apps:
        creds = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
        cred = credentials.Certificate(creds)
        firebase_admin.initialize_app(cred, {
            "storageBucket": f"{creds['project_id']}.appspot.com"
        })

def get_bucket():
    init_firebase()
    return storage.bucket()
