import logging
from logging.config import dictConfig

from fastapi import APIRouter, Depends, Path
from fastapi.params import Query
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request
from starlette.responses import JSONResponse

from main.config.log_config import LogConfig
from main.entity.final_response import FinalResponse
from main.service.abstract_weather_service import AbstractWeatherService
from main.service.weather_service import WeatherService
from main.utils.weather_constants import LOGGER_NAME

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)


dictConfig(LogConfig().model_dump())
logger = logging.getLogger(LOGGER_NAME)


@router.post("/weather/{city}", response_model=FinalResponse, response_model_exclude_none=True)
@limiter.limit("5/minute")
def post_weather_data(request: Request,
                      city: str = Path(..., description="The city to get weather data for"),
                      service: AbstractWeatherService = Depends(WeatherService)):
    logger.info("Received POST request with path : "+city)
    response = service.create_weather_data(city)
    return JSONResponse(content=response.model_dump(),
                        status_code=int(response.http_code))


@router.get("/weather", response_model_exclude_none=True)
@limiter.limit("5/minute")
def get_weather_data(request: Request,
                     date: str = Query(..., description="The date to get weather data for"),
                     service: AbstractWeatherService = Depends(WeatherService)):
    logger.info("Received GET request with date : "+date)
    response = service.get_weather_data(date)
    return JSONResponse(content=response.model_dump(),
                        status_code=int(response.http_code))
