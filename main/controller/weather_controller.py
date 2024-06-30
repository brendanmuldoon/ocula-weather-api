from logging.config import dictConfig
import logging
from main.config.log_config import LogConfig
from fastapi import APIRouter, Depends, Path
from fastapi.params import Query
from starlette.responses import JSONResponse

from main.entity.final_response import FinalResponse
from main.service.abstract_weather_service import AbstractWeatherService
from main.service.weather_service import WeatherService

router = APIRouter()

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("weather-api")


@router.post("/weather/{city}", response_model=FinalResponse, response_model_exclude_none=True)
def post_weather_data(city: str = Path(..., description="The city to get weather data for"),
                      service: AbstractWeatherService = Depends(WeatherService)):
    logger.info("Received POST request with path : "+city)
    response = service.create_weather_data(city)
    return JSONResponse(content=response.model_dump(),
                        status_code=int(response.http_code))


@router.get("/weather", response_model_exclude_none=True)
def get_weather_data(date: str = Query(..., description="The date to get weather data for"),
                     service: AbstractWeatherService = Depends(WeatherService)):
    logger.info("Received GET request with date : "+date)
    response = service.get_weather_data(date)
    print(response)
    return JSONResponse(content=response.model_dump(),
                        status_code=int(response.http_code))


@router.get("/db_query", response_model_exclude_none=True)
def get_weather_data(service: AbstractWeatherService = Depends(WeatherService)):  # delete once done
    service.get_all_data()
