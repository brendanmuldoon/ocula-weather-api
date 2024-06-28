from fastapi import Depends

from main.entity.weather_request import WeatherRequest
from main.repoository.abstract_weather_repository import AbstractWeatherRepository
from main.repoository.weather_repository import WeatherRepository


class WeatherService:

    def __init__(self, weather_repo: AbstractWeatherRepository = Depends(WeatherRepository)):
        self.weather_repo = weather_repo

    def get_weather(self, request: WeatherRequest):
        return self.weather_repo.post_weather_data(request=request)



