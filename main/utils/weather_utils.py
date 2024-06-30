from datetime import datetime

import pytz
from logging.config import dictConfig
import logging
from main.config.log_config import LogConfig
from main.entity.error_weather_response import ErrorResponse
from main.entity.final_response import FinalResponse
from main.entity.success_weather_response import SuccessResponse

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("weather-api")

def is_valid(data):
    return bool(data and data.strip())


def valid_weather_request(city: str):
    if bool(not is_valid(city)):
        logger.error("Request is invalid")
        return False
    return True


def is_successful_weather_api_client_response(open_weather_api_response):
    if bool(open_weather_api_response['cod'] == 200):
        return True
    logger.error(str(open_weather_api_response['message']))
    return False


def handle_error_response(message, code):
    return FinalResponse(
        http_code=code,
        data=ErrorResponse(error_message=message, http_code=code))


def create_cache_key(date: str):
    return f"{date}"


def create_cache_value(key, value):
    cache_value = {key: value}
    return cache_value


def get_date_from_epoch(date):
    utc_dt = datetime.utcfromtimestamp(int(date))
    uk_tz = pytz.timezone('Europe/London')
    uk_dt = utc_dt.astimezone(uk_tz)
    return uk_dt.date()


def create_cache_key_date(date):
    return get_date_from_epoch(date)


def create_dto_object(open_weather_api_response):
    logger.info("Creating database dto object")
    min_temp = open_weather_api_response['main']['temp_min'] - 273.15
    max_temp = open_weather_api_response['main']['temp_max'] - 273.15
    avg_temp = (min_temp + max_temp) / 2
    min_temp_formatted = f"{min_temp:.2f}"
    max_temp_formatted = f"{max_temp:.2f}"
    avg_temp_formatted = f"{avg_temp:.2f}"
    return SuccessResponse(
        http_code=str(open_weather_api_response["cod"]),
        city=str(open_weather_api_response['name']),
        date=str(get_date_from_epoch(str(open_weather_api_response['dt']))),
        min_temp=str(min_temp_formatted),
        max_temp=str(max_temp_formatted),
        avg_temp=str(avg_temp_formatted),
        humidity=str(open_weather_api_response['main']['humidity']))


def get_http_code_from_db_response(db_data):
    if isinstance(db_data, ErrorResponse):
        return db_data.http_code
    return "200"


def status_code_2xx(data):
    return bool(data.http_code == "201") or bool(data.http_code == "200")
