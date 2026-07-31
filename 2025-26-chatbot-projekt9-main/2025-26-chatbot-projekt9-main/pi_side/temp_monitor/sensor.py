from sense_hat import SenseHat
import subprocess

sense = SenseHat()

def get_cpu_temperature():
    output = subprocess.check_output(
        ["vcgencmd", "measure_temp"]
    ).decode()
    return float(output.replace("temp=", "").replace("'C\n", ""))

def read_temp():
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    raw = (t1 + t2) / 2

    cpu = get_cpu_temperature()
    compensated = raw - ((cpu - raw) / 1.5)

    return round(compensated, 2)
