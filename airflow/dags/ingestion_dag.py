import logging
import shutil
import os
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

# === Configuration ===
SOURCE_FOLDER = "/Users/ebotfabien/Desktop/school/air_new/raw-data"
DEST_FOLDER = "/Users/ebotfabien/Desktop/school/air_new/dags/destination"


@dag(
    dag_id="file_mover_dag",
    description="Move one file at a time from source to destination if it exists",
    tags=["file", "automation"],
    schedule=timedelta(minutes=1),  # Run every minute
    start_date=days_ago(0, hour=1),
    catchup=False,
    max_active_runs=1,
)
def file_mover_dag():
    """DAG that moves one file at a time from a source folder to a destination folder."""

    @task
    def move_file_if_exist():
        """Move only the first file found in SOURCE_FOLDER."""
        files = os.listdir(SOURCE_FOLDER)
        if not files:
            logging.info("No files to move.")
            return

        os.makedirs(DEST_FOLDER, exist_ok=True)

        # Take the first file only
        f = files[0]
        src_path = os.path.join(SOURCE_FOLDER, f)
        dest_path = os.path.join(DEST_FOLDER, f)
        if os.path.isfile(src_path):
            shutil.move(src_path, dest_path)
            logging.info(f"✅ Moved file: {f}")

    # Define DAG flow
    move_file_if_exist()


# Instantiate DAG
file_mover_dag_instance = file_mover_dag()
