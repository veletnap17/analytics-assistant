import os
from datetime import datetime
from dotenv import load_dotenv
from src.services.google_sheets_service import get_all_records

load_dotenv()

META_COLUMNS = {"Date", "Total Fleet", "", "Week", "Month"}

def get_fleet_rows():
    return get_all_records(os.getenv("FLEET_SHEET_ID"), os.getenv("FLEET_WORKSHEET"))

def get_latest_fleet():
    rows = [r for r in get_fleet_rows() if r.get("Date")]
    return max(rows, key=lambda r: datetime.strptime(r["Date"], "%d/%m/%Y"))

def get_fleet_size():
    return int(get_latest_fleet()["Total Fleet"])

def get_fleet_by_model():
    row = get_latest_fleet()
    return {
        k: v for k, v in row.items()
        if k not in META_COLUMNS and isinstance(v, (int, float)) and v > 0
    }

def get_fleet_size_excluding(excluded: list[str]):
    fleet = get_fleet_by_model()
    excluded = [x.lower() for x in excluded]
    return sum(v for model, v in fleet.items() if not any(x in model.lower() for x in excluded))

def get_fleet_change():
    rows = [r for r in get_fleet_rows() if r.get("Date")]
    rows.sort(key=lambda r: datetime.strptime(r["Date"], "%d/%m/%Y"), reverse=True)

    current = int(rows[0]["Total Fleet"])
    previous = int(rows[1]["Total Fleet"]) if len(rows) > 1 else current

    return {
        "current": current,
        "previous": previous,
        "change": current - previous,
        "date": rows[0]["Date"],
        "previous_date": rows[1]["Date"] if len(rows) > 1 else None
    }