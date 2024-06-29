from fastapi import APIRouter, Depends, Path
from fastapi.params import Query
from starlette.responses import JSONResponse

from main.entity.final_response import FinalResponse
from main.service.weather_service import WeatherService

router = APIRouter()


@router.post("/weather/{city}", response_model=FinalResponse, response_model_exclude_none=True)
def post_weather_data(city: str = Path(..., description="The city to get weather data for"),
                      service: WeatherService = Depends(WeatherService)):
    response = service.create_weather_data(city)
    return JSONResponse(content=response.model_dump(),
                        status_code=int(response.http_code))


@router.get("/weather", response_model_exclude_none=True)
def get_weather_data(date: str = Query(..., description="The date to get weather data for"),
                     service: WeatherService = Depends(WeatherService)):
    return service.get_weather_data(date)

# @router.get("/weather", response_model=WeatherResponse, response_model_exclude_none=True)
# def get_weather_data(date: str = Query(..., description="The date to get weather data for"),
#                      service: WeatherService = Depends(WeatherService)):
#     return service.get_weather_data(date)
