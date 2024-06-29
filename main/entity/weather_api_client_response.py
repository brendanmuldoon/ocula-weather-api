from pydantic import BaseModel
from typing import Optional


class WeatherApiClientResponse(BaseModel):
    city: Optional[str] = None
    date: Optional[str] = None
    min_temp: Optional[str] = None
    max_temp: Optional[str] = None
    avg_temp: Optional[str] = None
    humidity: Optional[str] = None
    http_code: str
    error_message: Optional[str] = None

    @classmethod
    def error(cls, error_message: str, http_code: str):
        return cls(
            city=None,
            date=None,
            min_temp=None,
            max_temp=None,
            avg_temp=None,
            humidity=None,
            http_code=http_code,
            error_message=error_message
        )

    @classmethod
    def get(cls, city: str, date: str, min_temp: str, max_temp: str, avg_temp: str, humidity: str, http_code: str):
        return cls(
            city=city,
            date=date,
            min_temp=min_temp,
            max_temp=max_temp,
            avg_temp=avg_temp,
            humidity=humidity,
            http_code=http_code,
            error_message=None
        )
