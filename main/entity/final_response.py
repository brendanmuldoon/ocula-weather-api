from typing import Union

from pydantic import BaseModel

from main.entity.error_weather_response import ErrorResponse
from main.entity.success_weather_response import SuccessResponse


class FinalResponse(BaseModel):
    http_code: str
    data: Union[SuccessResponse, ErrorResponse]