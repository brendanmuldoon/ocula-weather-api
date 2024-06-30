import pytest
from unittest.mock import patch, MagicMock
from main.client.weather_api_client import WeatherApiClient


@pytest.fixture
def weather_api_client():
    return WeatherApiClient()


@patch('requests.get')
def test_get_weather_success(mock_get, weather_api_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "name": "London",
        "temp": "100"
    }
    mock_get.return_value = mock_response

    city = "London"

    response = weather_api_client.get_weather(city)

    assert_response(mock_get, response, city, weather_api_client.base_url, weather_api_client.appid,
                    'temp', "100",
                    'name', "London")


@patch('requests.get')
def test_get_weather_failure(mock_get, weather_api_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "cod": "404",
        "message": "city not found"
    }
    mock_get.return_value = mock_response

    city = "UnknownCity"

    response = weather_api_client.get_weather(city)

    assert_response(mock_get, response, city, weather_api_client.base_url, weather_api_client.appid,
                    'cod', "404",
                    'message', "city not found")


def assert_response(mock_get, response, city, base_url, appid,
                    param_key_1, param_value_1,
                    param_key_2, param_value_2):
    assert mock_get.called
    assert mock_get.call_args[0][0] == base_url
    assert mock_get.call_args[1]['params']['q'] == city
    assert mock_get.call_args[1]['params']['appid'] == appid
    assert response[param_key_1] == param_value_1
    assert response[param_key_2] == param_value_2
