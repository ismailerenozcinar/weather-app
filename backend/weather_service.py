import requests
from fastapi import HTTPException

API_KEY = "API"

def get_coordinates(city_name: str, country_code="TR"):
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city_name,
        "limit": 5,
        "appid": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200 or not data:
        raise HTTPException(status_code=404, detail=f"{city_name} için koordinat bulunamadı.")

    for item in data:
        if item.get("country") == country_code:
            return item["lat"], item["lon"]

    return data[0]["lat"], data[0]["lon"]

def get_weather_for_city(city_name: str):
    lat, lon = get_coordinates(city_name)

    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,daily,alerts",
        "appid": API_KEY,
        "units": "metric",
        "lang": "tr"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f"{city_name} için hava durumu alınamadı.")

    return {
        "city": city_name,
        "lat": lat,
        "lon": lon,
        "current": response.json()["current"]
    }