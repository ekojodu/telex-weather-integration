from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv
import time
import threading

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["main"],
            "description": data["weather"][0]["description"]
        }
    else:
        return {"error": data.get("message", "Failed to get weather data")}

@app.get("/weather")
def fetch_weather(city: str = "Lagos"):
    """Fetches the current weather for a given city."""
    return get_weather(city)

@app.get("/weather_update")
def weather_update():
    """Returns a formatted weather update message."""
    return {"message": get_weather("Lagos")}

def send_weather_updates():
    while True:
        print(get_weather("Lagos"))  # Simulating updates
        time.sleep(3600)  # 1-hour interval

@app.on_event("startup")
def start_background_thread():
    threading.Thread(target=send_weather_updates, daemon=True).start()
