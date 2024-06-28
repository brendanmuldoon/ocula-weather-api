from main.entity.weather_request import WeatherRequest
from main.entity.weather_response import WeatherResponse
from main.repoository.abstract_weather_repository import AbstractWeatherRepository


class WeatherRepository(AbstractWeatherRepository):

    def post_weather_data(self, request: WeatherRequest):
        return WeatherResponse.get(date=request.date,
                                   city=request.city,
                                   min_temp="2",
                                   max_temp="3",
                                   avg_temp="4",
                                   humidity="10%",
                                   http_code="200")
