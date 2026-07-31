import os
import sys
import time
from datetime import datetime, timedelta
from sense_hat import SenseHat
from sensor import read_temp
from weather_service import get_weather
from logger import log_temperature, daily_summary, get_recent_days_summary
from alerts import check_alert
from config import TEMP_MONITOR_INTERVAL_MINUTES, ROOM_NAME
from datetime import datetime, timedelta
import csv
from haptic_game import run_haptic_game
from config import LOG_FILE
sys.stdout.reconfigure(encoding='utf-8')


degree = "\u00B0"
            
sense = SenseHat() 


def last_3_days_summary():
    """Prints temperature report for the last 3 days (same as --temp-report)."""
    days = 3
    summaries = get_recent_days_summary(days)
    if not summaries:
        print("No temperature data available for the last 3 days.")
        return

    today = datetime.now().date()
    recent_dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    
    print(f"\nTemperature report (local vs forecast) for last {days} days in {ROOM_NAME}:\n")
    for date, summary in zip(recent_dates, summaries):
        print(f"{date}:")
        print(f"  Local Temp   : min {summary['local_min']}{degree}C / max {summary['local_max']}{degree}C / difference {summary['local_diff']}{degree}C")
        print(f"  Forecast Temp: min {summary['forecast_min']}{degree}C / max {summary['forecast_max']}{degree}C / difference {summary['forecast_diff']}{degree}C\n")

def avg_temp_for_period(date, start, end, days=3):
    start_t = datetime.strptime(start, "%H:%M").time()
    end_t = datetime.strptime(end, "%H:%M").time()
    target_date = datetime.strptime(date, "%Y-%m-%d").date()

    temps = []

    # Read all rows from CSV
    rows = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
            delta_days = (target_date - ts.date()).days
            if 1 <= delta_days <= days:  # last N days before target date
                rows.append((ts, float(row["local_temp"])))

    if not rows:
        print("No readings available in the last {} days.".format(days))
        return

    # -----------------------------
    # Collect readings in the requested time window
    # -----------------------------
    for ts, temp in rows:
        if start_t <= ts.time() <= end_t:
            temps.append(temp)

    # -----------------------------
    # Option A: Average actual readings if they exist
    # -----------------------------
    if temps:
        print(round(sum(temps) / len(temps), 2))
        return

    # -----------------------------
    # Option B: Interpolate missing readings
    # -----------------------------
    # Convert start/end to datetime objects for each day
    interpolated_values = []
    for day_offset in range(1, days + 1):
        day_date = target_date - timedelta(days=day_offset)
        start_dt = datetime.combine(day_date, start_t)
        end_dt = datetime.combine(day_date, end_t)

        # Find nearest reading before start_dt and after end_dt
        before = [temp for ts, temp in rows if ts <= start_dt]
        after = [temp for ts, temp in rows if ts >= end_dt]

        if before and after:
            # Simple linear interpolation: avg of before/after
            interpolated_values.append((before[-1] + after[0]) / 2)
        elif before:
            interpolated_values.append(before[-1])
        elif after:
            interpolated_values.append(after[0])

    if interpolated_values:
        print(round(sum(interpolated_values) / len(interpolated_values), 2))
    else:
        print("No data available for this period.")

# ----------------------------------------
# MAIN MONITOR LOOP (live monitoring)
# ----------------------------------------
def monitor_loop():
    print(f"Temperature Monitoring Started for {ROOM_NAME} (every {TEMP_MONITOR_INTERVAL_MINUTES} minutes)\n")
    print("-> Press the Joystick at any time to start the Haptic Game!")
    while True:
        try:
            # 1. Perform Temperature Tasks
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            local_temp = read_temp()
            forecast_temp, desc = get_weather()
            log_temperature(local_temp, forecast_temp)

            # Display on LED
            sense.show_message(f"{local_temp}°C", scroll_speed=0.05)

            # Print Console Summary
            summary = daily_summary()
            if summary:
                print(f"{timestamp}: Local {local_temp}°C (Min: {summary['local_min']} / Max: {summary['local_max']})")
            
            # Check Alerts
            alert_msg = check_alert(local_temp, forecast_temp)
            if alert_msg:
                print(f"⚠️ ALERT: {alert_msg}")

            # 2. RESPONSIVE WAIT (Instead of time.sleep)
            # This loop runs for the duration of your interval (e.g., 30 mins)
            wait_seconds = TEMP_MONITOR_INTERVAL_MINUTES * 60
            start_wait = time.time()
            
            print(f"Waiting {TEMP_MONITOR_INTERVAL_MINUTES} minutes... (Joystick active)")
            
            while (time.time() - start_wait) < wait_seconds:
                # Check for Joystick events
                for event in sense.stick.get_events():
                    if event.action == "pressed":
                        print("🎮 Joystick pressed! Launching Haptic Game...")
                        run_haptic_game()
                        # After game ends, clear screen and resume waiting
                        sense.clear()
                        print("Resuming temperature monitor wait...")
                
                # Small sleep to prevent 100% CPU usage
                time.sleep(0.1)

        except KeyboardInterrupt:
            sense.clear()
            print("\nMonitoring stopped by user.")
            break
        except Exception as e:
            print(f"Error in monitor loop: {e}")
            time.sleep(10) # Wait a bit before retrying after error


# ----------------------------------------
# CLI ENTRY POINT
# ----------------------------------------
if __name__ == "__main__":
    import sys
    if "--temp-report" in sys.argv or "-r" in sys.argv:
        last_3_days_summary()
    elif "--avg-temp" in sys.argv:
        date = sys.argv[sys.argv.index("--date")+1]
        start = sys.argv[sys.argv.index("--start")+1]
        end = sys.argv[sys.argv.index("--end")+1]
        avg_temp_for_period(date, start, end)
    else:
        monitor_loop()