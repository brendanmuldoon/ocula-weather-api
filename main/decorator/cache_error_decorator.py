import sqlite3
import logging
from functools import wraps
from main.entity.error_weather_response import ErrorResponse
from main.utils.weather_constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def handle_cache_db_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        error_message = "Error occurred loading data into cache from DB :"
        try:
            return func(*args, **kwargs)
        except sqlite3.IntegrityError as e:
            error_message = "Integrity error occurred: " + str(e)
            logger.error(error_message)
            return []
        except sqlite3.OperationalError as e:
            error_message += str(e)
            logger.error(error_message)
            return []
        except sqlite3.DatabaseError as e:
            error_message += str(e)
            logger.error(error_message)
            return []
        except sqlite3.Error as e:
            error_message += str(e)
            logger.error(error_message)
            return []
        except Exception as e:
            error_message += str(e)
            logger.error(error_message)
            return []
    return wrapper
