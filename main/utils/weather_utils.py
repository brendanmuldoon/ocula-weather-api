from main.entity.weather_request import WeatherRequest
from main.entity.weather_response import WeatherResponse


def is_valid(data):
    return bool(data and data.strip())


def valid_weather_request(request: WeatherRequest):
    return bool(is_valid(request.date) and is_valid(request.city))


def is_successful_weather_api_client_response(open_weather_api_response):
    return bool(str(open_weather_api_response.__getattribute__('http_code')) == "200")


def handle_error_response(message, code):
    return WeatherResponse.error(error_message=message, http_code=code)
