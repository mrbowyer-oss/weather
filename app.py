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
            "latitude": 53.455,
            "longitude": -2.384,
            "current_weather": "true",
            "daily": "sunrise,sunset,precipitation_probability_max,windspeed_10m",
            "timezone": "Europe/London"
        })

        data = response.json()
        current = data["current_weather"]
        daily = data["daily"]

        # Convert daily average windspeed from m/s to mph
        wind_speed_mph = round(daily["windspeed_10m"][0] * 2.23694, 1)

        cached_weather = {
            "source": "open-meteo.com",
            "temperature": current["temperature"],
            "weather_code": current["weathercode"],
            "wind_speed": wind_speed_mph,
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
