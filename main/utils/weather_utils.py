from datetime import datetime

import pytz

from main.entity.error_weather_response import ErrorResponse
from main.entity.final_response import FinalResponse
from main.entity.success_weather_response import SuccessResponse


def is_valid(data):
    return bool(data and data.strip())


def valid_weather_request(city: str):
    return bool(is_valid(city))


def is_successful_weather_api_client_response(open_weather_api_response):
    return bool(open_weather_api_response['cod'] == 200)


def handle_error_response(message, code):
    return FinalResponse(
        http_code=code,
        data=ErrorResponse(error_message=message, http_code=code))


def create_cache_key(date: str):
    return f"{date}"


def create_cache_value(key, value):
    cache_value = {key: value}
    return cache_value


def create_cache_key_date(date):
    utc_dt = datetime.utcfromtimestamp(int(date))
    uk_tz = pytz.timezone('Europe/London')
    uk_dt = utc_dt.astimezone(uk_tz)
    return uk_dt.date()


def create_success_response(open_weather_api_response):
    min_temp = open_weather_api_response['main']['temp_min'] - 273.15
    max_temp = open_weather_api_response['main']['temp_max'] - 273.15
    avg_temp = (min_temp + max_temp) / 2
    min_temp_formatted = f"{min_temp:.2f}"
    max_temp_formatted = f"{max_temp:.2f}"
    avg_temp_formatted = f"{avg_temp:.2f}"
    return SuccessResponse(
        http_code=str(open_weather_api_response["cod"]),
        city=str(open_weather_api_response['name']),
        date=str(open_weather_api_response['dt']),
        min_temp=str(min_temp_formatted),
        max_temp=str(max_temp_formatted),
        avg_temp=str(avg_temp_formatted),
        humidity=str(open_weather_api_response['main']['humidity']))