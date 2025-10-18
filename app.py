from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Flask + Open-Meteo (with chance of rain) is live."

@app.route("/weather")
def weather():
    # Davyhulme Golf Club coordinates
    lat = "53.457"
    lon = "-2.384"
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&hourly=precipitation_probability"
        f"&daily=sunrise,sunset"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        current = data["current_weather"]
        daily = data["daily"]
        precip_chance = data["hourly"]["precipitation_probability"][0]

        result = {
            "temperature": round(current["temperature"]),
            "wind_speed": round(current["windspeed"], 1),
            "weather_code": current["weathercode"],
            "sunrise": daily["sunrise"][0],
            "sunset": daily["sunset"][0],
            "precip_chance": round(precip_chance),
            "source": "open-meteo.com"
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
