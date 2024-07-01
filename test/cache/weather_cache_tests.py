import unittest

import pytest

from main.cache.weather_cache import WeatherCache
from main.entity.success_weather_response import SuccessResponse
from test.test_utils.mock_db import MockDatabase


@pytest.fixture
def weather_cache():
    database = MockDatabase()
    cache = WeatherCache(database=database)
    return cache


def test_load_populates_cache_when_db_has_records(weather_cache):
    weather_cache.load()

    assert '2024-06-29' in weather_cache.cache
    assert 'London' in weather_cache.cache['2024-06-29']
    assert 'Paris' in weather_cache.cache['2024-06-29']

    london_weather = weather_cache.cache['2024-06-29']['London']
    paris_weather = weather_cache.cache['2024-06-29']['Paris']

    assert london_weather.city == 'London'
    assert london_weather.date == '2024-06-29'
    assert london_weather.min_temp == '15.5'
    assert london_weather.max_temp == '25.0'
    assert london_weather.avg_temp == '20.25'
    assert london_weather.humidity == '60'

    assert paris_weather.city == 'Paris'
    assert paris_weather.date == '2024-06-29'
    assert paris_weather.min_temp == '17.0'
    assert paris_weather.max_temp == '27.0'
    assert paris_weather.avg_temp == '22.0'
    assert paris_weather.humidity == '55'


def test_set_with_new_data(weather_cache):
    date_key = '2024-06-29'
    city_key = 'belfast'
    value = SuccessResponse(
        http_code="200",
        city="Belfast",
        date="2024-06-29",
        min_temp="15.5",
        max_temp="25.0",
        avg_temp="20.25",
        humidity="60"
    )
    weather_cache.set(date_key, city_key, value)
    assert len(weather_cache.cache) == 1


def test_set_with_existing_data(weather_cache):
    weather_cache.cache = {
        '2024-06-29': {
            'London': SuccessResponse(
                http_code="200",
                city="London",
                date="2024-06-29",
                min_temp="15.5",
                max_temp="25.0",
                avg_temp="20.25",
                humidity="60"
            )
        }
    }
    date_key = '2024-06-29'
    city_key = 'London'
    value = SuccessResponse(
        http_code="200",
        city="London",
        date="2024-06-29",
        min_temp="15.5",
        max_temp="25.0",
        avg_temp="20.25",
        humidity="60"
    )

    weather_cache.set(date_key, city_key, value)
    assert len(weather_cache.cache) == 1


def test_get_with_existing_data(weather_cache):
    # Adding data to the cache
    weather_cache.cache = {
        '2024-06-29': {
            'London': SuccessResponse(
                http_code="200",
                city="London",
                date="2024-06-29",
                min_temp="15.5",
                max_temp="25.0",
                avg_temp="20.25",
                humidity="60"
            ),
            'Paris': SuccessResponse(
                http_code="200",
                city="Paris",
                date="2024-06-29",
                min_temp="17.0",
                max_temp="27.0",
                avg_temp="22.0",
                humidity="55"
            )
        }
    }

    result = weather_cache.get('2024-06-29')
    assert len(result) == 2
    assert result[0].city == 'London'
    assert result[1].city == 'Paris'


def test_get_with_no_data(weather_cache):
    result = weather_cache.get('2024-06-30')
    assert result == []


if __name__ == '__main__':
    unittest.main()
