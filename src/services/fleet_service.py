import os
from datetime import datetime
from dotenv import load_dotenv
from src.services.google_sheets_service import get_all_records

load_dotenv()

META_COLUMNS = {"Date", "Total Fleet", "", "Week", "Month"}

def get_fleet_rows():
    return get_all_records(
        os.getenv("FLEET_SHEET_ID"),
        os.getenv("FLEET_WORKSHEET")
    )

def get_latest_fleet():
    rows = [r for r in get_fleet_rows() if r.get("Date")]
    return max(rows, key=lambda r: datetime.strptime(r["Date"], "%d/%m/%Y"))

def get_fleet_size():
    return get_latest_fleet()["Total Fleet"]

def get_fleet_by_model():
    row = get_latest_fleet()
    return {
        key: value
        for key, value in row.items()
        if key not in META_COLUMNS and isinstance(value, (int, float)) and value > 0
    }

def get_fleet_size_excluding(excluded: list[str]):
    fleet = get_fleet_by_model()
    excluded_lower = [x.lower() for x in excluded]

    return sum(
        value
        for model, value in fleet.items()
        if not any(x in model.lower() for x in excluded_lower)
    )