from contextlib import asynccontextmanager
from fastapi import FastAPI
from logging.config import dictConfig
import logging
from main.config.log_config import LogConfig
from main.cache.weather_cache_singleton import get_weather_cache
from main.controller import weather_controller
from main.utils.weather_constants import LOGGER_NAME

dictConfig(LogConfig().model_dump())
logger = logging.getLogger(LOGGER_NAME)

weather_cache = get_weather_cache()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Pre loading cache during application startup")
    weather_cache.load()
    yield
    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(weather_controller.router)