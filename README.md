![Contributors](https://img.shields.io/github/contributors/brendanmuldoon/cme-api-challenge)
![Issues](https://img.shields.io/github/issues/brendanmuldoon/cme-api-challenge)
[![Python 3.9](https://img.shields.io/badge/Python-3.9.6-blue.svg)](https://www.python.org)
[![FastAPI 0.111.0](https://img.shields.io/badge/FastAPI-0.111.0-blue.svg)](https://fastapi.tiangolo.com)
[![Version](https://img.shields.io/badge/Version-1.0.1-purple.svg)](https://your-project-url)

# Weather API

Welcome to the Weather API repository. This project provides a simple API for posting and retrieving weather data.

## API Documentation

This API is fully documented using Swagger. You can view and interact with the API documentation using the Swagger UI.

### [View Swagger API Documentation](https://brendanmuldoon.github.io/ocula-weather-api/)

## Starting The API

```bash
fastapi dev main/main.py # for local development

uvicorn main.main:app --host 0.0.0.0 --port 80 # for prod deployment

