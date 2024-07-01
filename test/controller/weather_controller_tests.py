import unittest
from unittest.mock import patch, MagicMock, create_autospec

import pytest
from starlette.testclient import TestClient

from main.controller.weather_controller import router
from main.main import app
from main.service.weather_service import WeatherService

app.include_router(router)


@pytest.fixture
def mock_weather_service():
    with patch('main.service.weather_service.WeatherService') as MockWeatherService:
        yield MockWeatherService


@pytest.fixture
def weather_client(mock_weather_service: MagicMock) -> TestClient:
    app.dependency_overrides[mock_weather_service] = create_autospec(lambda: None)
    return TestClient(app)


def test_post_weather_data(weather_client, mock_weather_service):
    mock_response = MagicMock()
    mock_response.model_dump.return_value = {
        "weather": "sunny",
        "http_code": "200"
    }
    mock_weather_service.create_weather_data.return_value = mock_response

    city = "London"

    response = weather_client.post("/weather/"+city)

    assert response.status_code == 200
    assert response.json() == {
        "weather": "sunny"
    }
    mock_weather_service.create_weather_data.assert_called_once_with(city)


def test_get_weather_data(weather_client: TestClient, mock_weather_service: MagicMock):
    mock_response = MagicMock()
    mock_response.model_dump.return_value = {
        "weather": "rainy",
        "http_code": "200"
    }
    mock_weather_service.get_weather_data.return_value = mock_response

    date = "2024-06-29"

    response = weather_client.get("/weather?date=2024-06-29")

    assert response.status_code == 200
    assert response.json() == {
        "weather": "rainy"
    }
    mock_weather_service.get_weather_data.assert_called_once_with(date)
