import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def get_google_client():
    credentials = Credentials.from_service_account_file(
        os.getenv("GOOGLE_CREDENTIALS_FILE"),
        scopes=SCOPES
    )
    return gspread.authorize(credentials)

def get_worksheet(sheet_id: str, worksheet_name: str):
    client = get_google_client()
    spreadsheet = client.open_by_key(sheet_id)
    return spreadsheet.worksheet(worksheet_name)

def get_all_records(sheet_id: str, worksheet_name: str):
    return get_worksheet(sheet_id, worksheet_name).get_all_records()