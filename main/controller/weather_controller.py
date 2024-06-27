from fastapi import APIRouter, HTTPException
from main.entity.weather_request import WeatherRequest
from main.entity.weather_response import WeatherResponse


router = APIRouter()


@router.post("/weather")
def create_weather_data(request: WeatherRequest):
    print(f"{request.city}_{request.date}")
    return WeatherResponse(date=request.date,
                           city=request.city,
                           min_temp="1",
                           max_temp="1",
                           avg_temp="1",
                           humidity="10%",
                           http_code="200",
                           error_message="")
