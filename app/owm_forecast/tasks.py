import logging

from app.owm_forecast.forecast_scripts.forecast_data import ForecastData
from config.celery import app

logger = logging.getLogger(__name__)


@app.task(name='app.owm_forecast.tasks.task_request_owm_data', ignore_result=True)
def task_request_owm_data() -> None:
    try:
        # todo: update to https://openweathermap.org/api/one-call-api
        ForecastData.do_owm_request(weather=True, air_pollution=True)
    except Exception as ex:
        logger.error(f"task_request_forecast_data(): {ex}")
