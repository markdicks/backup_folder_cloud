from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive']

creds = None

try:
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
except FileNotFoundError:
    pass

if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_config(
        {"installed": {
            "client_id": "203408454421-m7fngl1gaobp3thvb9hi6jr9j28lc958.apps.googleusercontent.com",
            "project_id": "",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "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",
            "redirect_uris": ["http://localhost:8080/"],
            "javascript_origins": []
        }},
        scopes=SCOPES,
            redirect_uri='http://localhost:8080/' #62941/
        )

    creds = flow.run_local_server(port=0)

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('drive', 'v3', credentials=creds)
