import gcsfs
import pandas as pd
from typing import Any, List
from fastapi import APIRouter, HTTPException
from api import schema
from api.config import get_settings

api_router = APIRouter()

fs = gcsfs.GCSFileSystem(
    project=get_settings().GCP_PROJECT,
    token=get_settings().GCP_SERVICE_ACCOUNT_JSON_PATH
)

# # Konfigurasi GCSFS dengan kredensial GCP
# gcs = gcsfs.GCSFileSystem(project=get_settings().GCP_PROJECT, token="google_default")

@api_router.get("/health", response_model=schema.Health, status_code=200)
def health() -> dict:
    """ Health check endpoint """

    health_data = schema.Health(
        name=get_settings().PROJECT_NAME, api_version=get_settings().VERSION
    )
    return health_data.dict()


@api_router.get("/consumer_type_values", response_model=schema.UniqueConsumerType, status_code=200)
def consumer_type_values() -> List:
    """Get unique value for type consumer"""

    # Download from GCS
    file_path = f"{get_settings().GCP_BUCKET}/X.csv"
    # read file CSV from GCP bucket
    data = pd.read_csv(fs.open(file_path), parse_dates=['datetime_utc'])
    unique_consumer_type = list(data["consumer_type"].unique())
    return {"values": unique_consumer_type}


@api_router.get("/area_values", response_model=schema.UniqueArea, status_code=200)
def area_values() -> List:
    """ Get unique value for area """

    # Download the data from GCS.
    file_path = f"{get_settings().GCP_BUCKET}/X.csv"
    data = pd.read_csv(fs.open(file_path), parse_dates=['datetime_utc'])
    unique_area = list(data["area"].unique())
    return {"values": unique_area}


@api_router.get(
    "/predictions/{area}/{consumer_type}",
    response_model=schema.PredictionResult,
    status_code=200
)
async def predictions(area: int, consumer_type: int) -> Any:
    """
    get predictions from data
    area and type consumer
    """
 
    # Download data dari GCS
    train_path = f"{get_settings().GCP_BUCKET}/y.csv"
    train_df = pd.read_csv(
        fs.open(train_path), 
        parse_dates=['datetime_utc'],
        index_col=['area', 'consumer_type', 'datetime_utc']
    )
    preds_path = f"{get_settings().GCP_BUCKET}/predictions.csv"
    preds_df = pd.read_csv(
        fs.open(preds_path), 
        parse_dates=['datetime_utc'],
        index_col=['area', 'consumer_type', 'datetime_utc']
    )

    # Query the data for the given area and consumer type.
    try:
        train_df = train_df.xs((area, consumer_type), level=["area", "consumer_type"])
        preds_df = preds_df.xs((area, consumer_type), level=["area", "consumer_type"])
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for the given area and consumer type: {area}, {consumer_type}",
        )
 
    if len(train_df) == 0 or len(preds_df) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for the given area and consumer type: {area}, {consumer_type}",
        )
    
    # Return only the latest week of observations.
    train_df = train_df.sort_index().tail(24 * 7)
    preds_df = preds_df.sort_index().tail(24 * 7)

    # Prepare data to be returned.
    datetime_utc = train_df.index.get_level_values("datetime_utc").to_list()
    energy_consumption = train_df["energy_consumption"].to_list()

    preds_datetime_utc = preds_df.index.get_level_values("datetime_utc").to_list()
    preds_energy_consumption = preds_df["energy_consumption"].to_list()

    results = {
        "datetime_utc": datetime_utc,
        "energy_consumption": energy_consumption,
        "preds_datetime_utc": preds_datetime_utc,
        "preds_energy_consumption": preds_energy_consumption,
    }

    return results


@api_router.get(
    "/monitoring/metrics",
    response_model=schema.MonitoringMetrics,
    status_code=200
)
async def get_metrics() -> Any:
    """Get metrics from monitoring."""

    # Download data dari GCS
    file_path = f"{get_settings().GCP_BUCKET}/metrics_monitoring.csv"
    metrics = pd.read_csv(
        fs.open(file_path),
        parse_dates=['datetime_utc'],
        index_col=['datetime_utc']
    )

    datetime_utc = metrics.index.to_list()
    mape = metrics["MAPE"].to_list()

    return {
        "datetime_utc": datetime_utc,
        "mape": mape,
    }


@api_router.get(
    "/monitoring/values/{area}/{consumer_type}",
    response_model=schema.MonitoringValues,
    status_code=200
)
async def get_predictions(area: int, consumer_type: int) -> Any:
    """
    Get forecasted predictions based on the given area and consumer type.
    """

    # Download data dari GCS.
    y_path = f"{get_settings().GCP_BUCKET}/y_monitoring.csv"
    y_monitoring = pd.read_csv(
        fs.open(y_path),
        parse_dates=['datetime_utc'], 
        index_col=['area', 'consumer_type', 'datetime_utc']
    )
    preds_path = f"{get_settings().GCP_BUCKET}/predictions_monitoring.csv"
    predictions_monitoring = pd.read_csv(
        fs.open(preds_path),
        parse_dates=['datetime_utc'],
        index_col=['area', 'consumer_type', 'datetime_utc']
    )

    # Query the data for the given area and consumer type.
    try:
        y_monitoring = y_monitoring.xs(
            (area, consumer_type), level=["area", "consumer_type"]
        )
        predictions_monitoring = predictions_monitoring.xs(
            (area, consumer_type), level=["area", "consumer_type"]
        )
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for the given area and consumer typefrontend: {area}, {consumer_type}",
        )

    if len(y_monitoring) == 0 or len(predictions_monitoring) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for the given area and consumer type: {area}, {consumer_type}",
        )
    
    # Prepare data to be returned.
    y_monitoring_datetime_utc = y_monitoring.index.get_level_values(
        "datetime_utc"
    ).to_list()
    y_monitoring_energy_consumption = y_monitoring["energy_consumption"].to_list()

    predictions_monitoring_datetime_utc = predictions_monitoring.index.get_level_values(
        "datetime_utc"
    ).to_list()
    predictions_monitoring_energy_consumptionc = predictions_monitoring[
        "energy_consumption"
    ].to_list()

    results = {
        "y_monitoring_datetime_utc": y_monitoring_datetime_utc,
        "y_monitoring_energy_consumption": y_monitoring_energy_consumption,
        "predictions_monitoring_datetime_utc": predictions_monitoring_datetime_utc,
        "predictions_monitoring_energy_consumptionc": predictions_monitoring_energy_consumptionc,
    }

    return results

