from contextlib import asynccontextmanager

from fastapi import FastAPI

from main.cache.weather_cache_singleton import get_weather_cache
from main.controller import weather_controller

weather_cache = get_weather_cache()


@asynccontextmanager
async def lifespan(app: FastAPI):
    weather_cache.load()
    yield
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(weather_controller.router)