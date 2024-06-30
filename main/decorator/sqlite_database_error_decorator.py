import sqlite3
import logging
from functools import wraps
from main.entity.error_weather_response import ErrorResponse
from main.utils.weather_constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def handle_sqlite_db_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.IntegrityError as e:
            error_message = "Integrity error occurred: " + str(e)
            logger.error(error_message)
            return ErrorResponse(error_message=error_message, http_code="400")
        except sqlite3.OperationalError as e:
            error_message = "Operational error occurred: " + str(e)
            logger.error(error_message)
            return ErrorResponse(error_message=error_message, http_code="500")
        except sqlite3.DatabaseError as e:
            error_message = "Database error occurred: " + str(e)
            logger.error(error_message)
            return ErrorResponse(error_message=error_message, http_code="500")
        except sqlite3.Error as e:
            error_message = "An error occurred: " + str(e)
            logger.error(error_message)
            return ErrorResponse(error_message=error_message, http_code="500")
        except Exception as e:
            error_message = "An unexpected error occurred: " + str(e)
            logger.error(error_message)
            return ErrorResponse(error_message=error_message, http_code="500")
    return wrapper
