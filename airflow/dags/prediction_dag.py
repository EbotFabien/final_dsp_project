from __future__ import annotations
from airflow.decorators import dag, task
from airflow.utils.state import State
from airflow.models import DagRun
from pendulum import datetime
from pathlib import Path
import pandas as pd, requests, json

from lib.io_utils import data_root
from lib.db_utils import mark_processed, unprocessed_good_files
from airflow.models import Variable

API_BASE = Variable.get("MODEL_API_BASE", "http://model-api:8000")

@dag(
    schedule="*/2 * * * *",  # every 2 min
    start_date=datetime(2025,1,1),
    catchup=False,
    tags=["ds-prod","prediction"],
    max_active_runs=1,
)
def prediction_dag():
    @task
    def check_for_new_data() -> list[str]:
        good = list((data_root()/ "good_data").glob("*.csv"))
        good = [str(p) for p in good]
        todo = unprocessed_good_files(good)
        return todo

    @task
    def skip_or_go(paths: list[str]) -> str:
        return "make_predictions" if paths else "skip_run"

    @task
    def skip_run():
        # Mark the dag run as skipped (Airflow 2.x: set all tasks skipped).
        # The UI will show DAG run 'success' by default; we can short-circuit by not raising.
        return "no_new_data"

    @task
    def make_predictions(paths: list[str]):
        for fp in paths:
            df = pd.read_csv(fp)
            payload = {
                "source": "scheduled",   # so UI can filter
                "records": df.to_dict(orient="records")
            }
            r = requests.post(f"{API_BASE}/predict", json=payload, timeout=30)
            r.raise_for_status()
            mark_processed(fp)

    paths = check_for_new_data()
    _ = skip_or_go(paths)
    make_predictions(paths)
    skip_run()

prediction_dag()
