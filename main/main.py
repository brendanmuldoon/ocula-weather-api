from fastapi import FastAPI

from main.controller import weather_controller

app = FastAPI()

app.include_router(weather_controller.router)

