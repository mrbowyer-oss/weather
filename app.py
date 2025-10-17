from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Flask + OpenWeather is live."

@app.route("/weather")
def weather():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    lat = "53.457"
    lon = "-2.384"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        result = {
            "location": data.get("name"),
            "temperature": round(data["main"]["temp"]),
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "wind_speed": data["wind"]["speed"],
            "wind_deg": data["wind"]["deg"],
            "sunrise": data["sys"]["sunrise"],
            "sunset": data["sys"]["sunset"]
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
