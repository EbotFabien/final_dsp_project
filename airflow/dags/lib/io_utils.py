from pathlib import Path
import hashlib
import pandas as pd
from airflow.models import Variable

def data_root() -> Path:
    return Path(Variable.get("DATA_ROOT", "/opt/airflow/data"))

def pick_random_file():
    import random
    raw = data_root() / "raw_data"
    files = [p for p in raw.glob("*.csv") if p.is_file()]
    return random.choice(files) if files else None

def file_sha1(p: Path) -> str:
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def split_by_mask(df: pd.DataFrame, mask_valid, base_name: str, out_good: Path, out_bad: Path):
    out_good.mkdir(parents=True, exist_ok=True)
    out_bad.mkdir(parents=True, exist_ok=True)

    if len(df) == int(mask_valid.sum()):
        good_path = out_good / f"{base_name}"
        df.to_csv(good_path, index=False)
        return str(good_path), None

    if int(mask_valid.sum()) == 0:
        bad_path = out_bad / f"{base_name}"
        df.to_csv(bad_path, index=False)
        return None, str(bad_path)

    good_path = out_good / f"{base_name.replace('.csv','_good.csv')}"
    bad_path  = out_bad  / f"{base_name.replace('.csv','_bad.csv')}"
    df[mask_valid].to_csv(good_path, index=False)
    df[~mask_valid].to_csv(bad_path, index=False)
    return str(good_path), str(bad_path)
