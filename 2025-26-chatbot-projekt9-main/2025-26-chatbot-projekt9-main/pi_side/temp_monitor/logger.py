# logger.py (updated)

import csv
import os
import sys
from datetime import datetime, timedelta
from config import LOG_FILE
sys.stdout.reconfigure(encoding='utf-8')


def init_csv():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "local_temp", "forecast_temp"])

def log_temperature(local_temp, forecast_temp):
    init_csv()
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         round(local_temp,2),
                         round(forecast_temp,2)])

def daily_summary():
    recent = get_recent_days_summary(1)
    if recent:
        return recent[0]  # get first (most recent) day's summary
    return None

# --------------------------
# NEW: RECENT DAYS SUMMARY
# --------------------------
def get_recent_days_summary(days=3):
    """Return min/max/difference for last `days` days for both local and forecast"""
    if not os.path.exists(LOG_FILE):
        return {}

    summaries = {}  # key=date string, value=dict with min/max/diff

    today = datetime.now().date()
    recent_dates = [(today - timedelta(days=i)) for i in range(days)]

    # Initialize summaries
    for d in recent_dates:
        date_str = d.strftime("%Y-%m-%d")
        summaries[date_str] = {
            "local_min": None,
            "local_max": None,
            "local_diff": None,
            "forecast_min": None,
            "forecast_max": None,
            "forecast_diff": None
        }

    # Read CSV
    with open(LOG_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
            date_str = ts.date().strftime("%Y-%m-%d")
            if date_str not in summaries:
                continue

            local = float(row["local_temp"])
            forecast = float(row["forecast_temp"])

            # Update local min/max
            s = summaries[date_str]
            s["local_min"] = local if s["local_min"] is None else min(s["local_min"], local)
            s["local_max"] = local if s["local_max"] is None else max(s["local_max"], local)
            s["forecast_min"] = forecast if s["forecast_min"] is None else min(s["forecast_min"], forecast)
            s["forecast_max"] = forecast if s["forecast_max"] is None else max(s["forecast_max"], forecast)

    # Compute differences
    for s in summaries.values():
        if s["local_min"] is not None:
            s["local_diff"] = round(s["local_max"] - s["local_min"], 2)
            s["forecast_diff"] = round(s["forecast_max"] - s["forecast_min"], 2)

    # Return as list ordered by date descending
    return [summaries[d.strftime("%Y-%m-%d")] for d in recent_dates]
