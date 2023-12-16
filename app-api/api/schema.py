from typing import Any, List
from pydantic import BaseModel
import datetime


class Health(BaseModel):
    name: str
    api_version: str

#<=======================================================================>
class UniqueConsumerType(BaseModel):
    values: List[int]


class UniqueArea(BaseModel):
    values: List[int]


class PredictionResult(BaseModel):
    datetime_utc: List[datetime.datetime]
    energy_consumption: List[float]
    preds_datetime_utc: List[datetime.datetime]
    preds_energy_consumption: List[float]

#<========================================================================>
class MonitoringMetrics(BaseModel):
    datetime_utc: List[datetime.datetime]
    mape: List[float]


class MonitoringValues(BaseModel):
    y_monitoring_datetime_utc: List[datetime.datetime]
    y_monitoring_energy_consumption: List[float]
    predictions_monitoring_datetime_utc: List[datetime.datetime]
    predictions_monitoring_energy_consumptionc: List[float]