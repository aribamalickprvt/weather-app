from http.server import BaseHTTPRequestHandler
import httpx
import os
import json

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        city = self.path.split("/")[-1]
        response = httpx.get(
            f"{BASE_URL}/weather",
            params={"q": city, "appid": API_KEY, "units": "metric"}
        )
        self.send_response(response.status_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if response.status_code == 200:
            data = response.json()
            result = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],
                "wind_speed": data["wind"]["speed"],
                "visibility": data.get("visibility", 0) // 1000,
                "pressure": data["main"]["pressure"],
            }
            self.wfile.write(json.dumps(result).encode())
        else:
            self.wfile.write(json.dumps({"detail": "City not found"}).encode())