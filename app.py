from flask import Flask, jsonify
from flask_cors import CORS
import requests
import datetime

app = Flask(__name__)
CORS(app)

# Cache store
cached_weather = None
cached_time = None

@app.route("/")
def home():
    return "✅ Weather app is live."

@app.route("/weather")
def fetch_weather():
    global cached_weather, cached_time
    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": 53.455,  # Update to your correct location
            "longitude": -2.384,
            "current": "temperature_2m,weather_code,wind_speed_10m",
            "daily": "sunrise,sunset,precipitation_probability_max",
            "timezone": "Europe/London"
        })

        data = response.json()
        current = data["current"]
        daily = data["daily"]

        cached_weather = {
            "source": "open-meteo.com",
            "temperature": current["temperature_2m"],
            "weather_code": current["weather_code"],
            "wind_speed": current["wind_speed"],
            "precip_chance": daily["precipitation_probability_max"][0],
            "sunrise": daily["sunrise"][0],
            "sunset": daily["sunset"][0]
        }
        cached_time = datetime.datetime.utcnow()
        return jsonify(cached_weather)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/cached-weather")
def get_cached_weather():
    global cached_weather
    if cached_weather:
        return jsonify(cached_weather)
    else:
        return jsonify({"error": "No cached weather available."}), 404
