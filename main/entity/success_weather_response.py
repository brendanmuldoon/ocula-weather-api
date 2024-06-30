from typing import Optional

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    city: Optional[str] = None
    date: Optional[str] = None
    min_temp: Optional[str] = None
    max_temp: Optional[str] = None
    avg_temp: Optional[str] = None
    humidity: Optional[str] = None
