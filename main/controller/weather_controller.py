from fastapi import APIRouter, Depends

from main.entity.weather_request import WeatherRequest
from main.entity.weather_response import WeatherResponse
from main.service.weather_service import WeatherService

router = APIRouter()


@router.post("/weather", response_model=WeatherResponse, response_model_exclude_none=True)
def post_weather_data(request: WeatherRequest, service: WeatherService = Depends(WeatherService)):
    return service.create_weather_data(request)

