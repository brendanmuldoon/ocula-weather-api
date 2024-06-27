from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    date: str
    min_temp: str
    max_temp: str
    avg_temp: str
    humidity: str
    http_code: str
    error_message: str

