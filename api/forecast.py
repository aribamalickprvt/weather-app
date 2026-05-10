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
            f"{BASE_URL}/forecast",
            params={"q": city, "appid": API_KEY, "units": "metric", "cnt": 5}
        )
        self.send_response(response.status_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if response.status_code == 200:
            data = response.json()
            forecast = [{"time": i["dt_txt"], "temperature": round(i["main"]["temp"]), "description": i["weather"][0]["description"].title(), "icon": i["weather"][0]["icon"]} for i in data["list"]]
            self.wfile.write(json.dumps({"forecast": forecast}).encode())
        else:
            self.wfile.write(json.dumps({"detail": "City not found"}).encode())