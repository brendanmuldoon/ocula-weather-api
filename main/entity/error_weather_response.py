from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error_message: str
    http_code: str
