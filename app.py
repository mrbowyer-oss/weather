from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Flask + Open-Meteo is live."

@app.route("/weather")
def weather():
    # Davyhulme, UK coordinates
    lat = "53.453"
    lon = "2.369"
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,wind_speed_10m,weather_code"
        f"&daily=sunrise,sunset"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        current = data["current"]
        daily = data["daily"]

        result = {
            "temperature": round(current["temperature_2m"]),
            "wind_speed": round(current["wind_speed_10m"], 1),
            "weather_code": current["weather_code"],
            "sunrise": daily["sunrise"][0],
            "sunset": daily["sunset"][0],
            "source": "open-meteo.com"
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
