from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "13f8cd8b5f78721aa60fd3102652ebd7"
BASE_URL = "https://api.openweathermap.org/data/2.5"

@app.get("/")
def root():
    return {"message": "Weather API is running"}

@app.get("/weather/{city}")
async def get_weather(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/weather",
            params={"q": city, "appid": API_KEY, "units": "metric"}
        )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="City not found")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Weather API error")
    data = response.json()
    return {
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

@app.get("/forecast/{city}")
async def get_forecast(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/forecast",
            params={"q": city, "appid": API_KEY, "units": "metric", "cnt": 5}
        )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="City not found")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Weather API error")
    data = response.json()
    forecast = []
    for item in data["list"]:
        forecast.append({
            "time": item["dt_txt"],
            "temperature": round(item["main"]["temp"]),
            "description": item["weather"][0]["description"].title(),
            "icon": item["weather"][0]["icon"],
        })
    return {"forecast": forecast}
