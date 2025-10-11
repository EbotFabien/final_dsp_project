import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"  # Update if running on another host

def make_predictions(data: pd.DataFrame):
    """Send features to FastAPI API for prediction."""
    features = data.to_dict(orient="records")
    response = requests.post(f"{API_URL}/predict", json={"features": features})
    response.raise_for_status()
    return response.json()["predictions"]

def get_past_predictions(source="all", start_date=None, end_date=None):
    """Fetch past predictions (for visualization)."""
    params = {"source": source, "start_date": start_date, "end_date": end_date}
    response = requests.get(f"{API_URL}/past-predictions", params=params)
    response.raise_for_status()
    return response.json()