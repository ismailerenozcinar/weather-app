from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import CityRequest
from weather_service import get_weather_for_city

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/weather/default")
def get_default_city_weather():
    return get_weather_for_city("Ankara")

@app.post("/weather")
def get_weather_for_requested_city(data: CityRequest):
    return get_weather_for_city(data.city)
