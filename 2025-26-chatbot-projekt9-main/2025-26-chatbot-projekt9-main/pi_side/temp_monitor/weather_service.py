import requests
from config import WEATHER_API_KEY, CITY, COUNTRY_CODE

def get_weather():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY},{COUNTRY_CODE}&appid={WEATHER_API_KEY}&units=metric"
    )

    response = requests.get(url, timeout=10)
    data = response.json()

    temp = round(data["main"]["temp"], 2)
    desc = data["weather"][0]["description"]

    return temp, desc
