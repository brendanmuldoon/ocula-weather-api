from main.entity.weather_request import WeatherRequest


def is_valid(data):
    return bool(data and data.strip())


def verify_valid_payload(request: WeatherRequest):
    return bool(is_valid(request.date) and is_valid(request.city))