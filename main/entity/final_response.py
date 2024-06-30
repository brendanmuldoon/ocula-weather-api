from typing import Union, TypeVar, Generic, List

from pydantic import BaseModel

from main.entity.error_weather_response import ErrorResponse
from main.entity.success_weather_response import SuccessResponse


class FinalResponse(BaseModel):
    http_code: str
    data: Union[List[SuccessResponse], ErrorResponse]
