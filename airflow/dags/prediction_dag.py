import logging
import os
import math
import json
import shutil
import glob
import requests
import pandas as pd
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

# === Configuration ===
DATA_DIR = "/Users/ebotfabien/Desktop/school/air_new/dags/destination"
PROCESSED_PATH = "/Users/ebotfabien/Desktop/school/air_new/processed"
API_URL = "http://127.0.0.1:8000/predict_batch/"
BATCH_SIZE = 10  # rows per request


@dag(
    dag_id="predict_batch_dag",
    description="Check for CSVs, send them to API in batches, and move processed files.",
    schedule_interval=timedelta(seconds=5),  # Runs every 5 seconds
    start_date=days_ago(0, hour=1),
    catchup=False,
    max_active_runs=1,  # Avoid queue stacking
    tags=["machine_learning", "batch_prediction"],
)
def predict_batch_dag():
    """DAG to send CSV data in batches to an API."""

    @task
    def send_batch_predictions():
        # Find CSV files in the data directory
        csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
        if not csv_files:
            logging.info(f"⚠️ No CSV files found in {DATA_DIR}")
            return

        CSV_PATH = csv_files[0]
        logging.info(f"📄 Found CSV file: {CSV_PATH}")

        # Read CSV
        try:
            df = pd.read_csv(CSV_PATH)
        except Exception as e:
            logging.error(f"❌ Error reading CSV: {e}")
            return

        if df.empty:
            logging.warning(f"⚠️ File {CSV_PATH} is empty — skipping.")
            return

        # Validate required columns
        required_cols = [
            "squareMeters", "numberOfRooms", "hasYard", "hasPool", "floors",
            "cityCode", "cityPartRange", "numPrevOwners", "made", "isNewBuilt",
            "hasStormProtector", "basement", "attic", "garage",
            "hasStorageRoom", "hasGuestRoom"
        ]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            logging.error(f"❌ Missing required columns: {missing}")
            return

        # Send data in batches
        num_batches = math.ceil(len(df) / BATCH_SIZE)
        logging.info(f"📦 Sending {num_batches} batch(es)...")

        for i in range(num_batches):
            batch = df.iloc[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
            payload = batch.to_dict(orient="records")
            logging.info(f"📦 Sending batch {i+1}/{num_batches}")

            try:
                response = requests.post(API_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    logging.info(f"✅ Batch {i+1}/{num_batches} successful!")
                else:
                    logging.error(f"❌ Batch {i+1}/{num_batches} failed: {response.status_code}")
            except requests.exceptions.RequestException as e:
                logging.error(f"🚨 Error sending batch {i+1}: {e}")

        

    send_batch_predictions()


# Instantiate DAG
predict_batch_dag_instance = predict_batch_dag()
