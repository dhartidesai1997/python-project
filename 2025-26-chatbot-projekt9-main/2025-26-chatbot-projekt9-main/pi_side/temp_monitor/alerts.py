from config import TEMP_ALERT_THRESHOLD


degree = "\u00B0"
def check_alert(local, forecast):
    diff = abs(local - forecast)
    if diff >= TEMP_ALERT_THRESHOLD:
        return f"Temperature difference {diff:.2f}{degree}C exceeds threshold!"
    return None
