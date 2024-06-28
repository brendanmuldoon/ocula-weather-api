from fastapi import APIRouter, Depends

from main.entity.weather_request import WeatherRequest
from main.entity.weather_response import WeatherResponse
from main.service.weather_service import WeatherService

router = APIRouter()


@router.post("/weather", response_model=WeatherResponse)
def post_weather_data(request: WeatherRequest, service: WeatherService = Depends(WeatherService)):
    print(f"{request.city}_{request.date}")
    return service.get_weather(request)

