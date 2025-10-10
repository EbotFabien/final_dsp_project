from __future__ import annotations
from airflow.decorators import dag, task
from pendulum import datetime
from pathlib import Path
import pandas as pd, json

from lib.io_utils import pick_random_file, data_root, split_by_mask
from lib.validators import validate_df
from lib.db_utils import insert_ingestion_stats
from lib.alerts import send_teams_alert

@dag(
    schedule="* * * * *",  # every 1 min
    start_date=datetime(2025,1,1),
    catchup=False,
    tags=["ds-prod","ingestion"],
    max_active_runs=1,
)
def ingestion_dag():
    @task
    def read_data() -> str | None:
        p = pick_random_file()
        return str(p) if p else None

    @task.branch()
    def has_file(file_path: str | None) -> str:
        return "validate_data" if file_path else "no_file"

    @task
    def no_file():
        return "nothing_to_do"

    @task(task_id="validate_data")
    def validate_data(file_path: str) -> dict:
        df = pd.read_csv(file_path)
        mask, errors, criticality = validate_df(df)

        report_dir = data_root()/ "reports"; report_dir.mkdir(exist_ok=True, parents=True)
        report_path = report_dir / (Path(file_path).stem + "_report.html")
        html = f"<h2>Validation report - {file_path}</h2><p>criticality: {criticality}</p><pre>{json.dumps(errors, indent=2)}</pre>"
        report_path.write_text(html, encoding="utf-8")

        return {
            "file_path": file_path,
            "filename": Path(file_path).name,
            "total_rows": int(len(df)),
            "valid_rows": int(mask.sum()),
            "invalid_rows": int((~mask).sum()),
            "criticality": criticality,
            "errors": errors,
            "mask_valid": mask.tolist(),
            "report_path": str(report_path),
        }

    @task
    def save_statistics(info: dict):
        insert_ingestion_stats(
            info["filename"],
            info["total_rows"], info["valid_rows"], info["invalid_rows"],
            info["criticality"], json.dumps(info["errors"])
        )

    @task
    def send_alerts(info: dict):
        if info["invalid_rows"] > 0:
            sev = "error" if info["criticality"]=="high" else ("warning" if info["criticality"]=="medium" else "info")
            summary = (f"{info['filename']} — rows: {info['total_rows']}, "
                       f"invalid: {info['invalid_rows']} ({info['criticality']}).")
            send_teams_alert("Data quality alert", summary, sev, link=info["report_path"])

    @task
    def split_and_save_data(info: dict):
        df = pd.read_csv(info["file_path"])
        mask = pd.Series(info["mask_valid"])
        root = data_root()
        good, bad = split_by_mask(
            df, mask, Path(info["file_path"]).name, root/"good_data", root/"bad_data"
        )
        Path(info["file_path"]).unlink(missing_ok=True)
        return {"good_path": good, "bad_path": bad}

    file_path = read_data()
    _ = has_file(file_path)
    v = validate_data(file_path)
    # fan out
    [save_statistics(v), send_alerts(v), split_and_save_data(v)]
    no_file()

ingestion_dag()
