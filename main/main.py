from fastapi import FastAPI

from main.cache.weather_cache_singleton import get_weather_cache
from main.controller import weather_controller
from contextlib import asynccontextmanager
from contextlib import asynccontextmanager

from fastapi import FastAPI

from main.cache.weather_cache_singleton import get_weather_cache
from main.controller import weather_controller

# Initialize the weather cache
weather_cache = get_weather_cache()


@asynccontextmanager
async def lifespan(app: FastAPI):
    weather_cache.load()
    # Yield to allow the application to run
    yield
    # Shutdown even
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(weather_controller.router)