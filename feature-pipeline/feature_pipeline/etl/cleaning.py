import pandas as pd
from sklearn.preprocessing import LabelEncoder


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns to match our schema.
    """
    data = df.copy()
    data.drop(columns=["HourDK", "DK36Title", "DK19Title"], inplace=True)
    data.rename(
        columns={
            "HourUTC": "datetime_utc",
            "DK36Code": "area",
            "DK19Code": "consumer_type",
            "Consumption_MWh": "energy_consumption"
        }, inplace=True
    )

    return data

def cast_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cast columns to the correct data type.
    """
 
    data = df.copy()
    data["datetime_utc"] = pd.to_datetime(data["datetime_utc"])
    data["area"] = data["area"].astype("string")
    data["consumer_type"] = data["consumer_type"].astype("string")
    data["energy_consumption"] = data["energy_consumption"].astype("float64")

    return data

def encode_area_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode the area column to integers.
    """
 
    data = df.copy()
    
    label_encoder = LabelEncoder()
    data['area'] = label_encoder.fit_transform(data['area'])
    data['consumer_type'] = label_encoder.fit_transform(data['consumer_type'])

    data["area"] = data["area"].astype("int8")
    data['consumer_type'] = data['consumer_type'].astype("int8")
    return data