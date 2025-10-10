import pandas as pd

REQUIRED = ["age","country","amount"]
COUNTRIES = {"China","India","Lebanon"}  # keep strict to trigger 'unknown'

def row_is_valid(row):
    errs = {}
    for c in REQUIRED:
        if c not in row or pd.isna(row[c]):
            errs[c] = "missing"
    if "age" in row:
        try:
            if int(float(row["age"])) < 0:
                errs["age"] = "negative"
        except Exception:
            errs["age"] = "non_numeric"
    if "country" in row and pd.notna(row["country"]):
        if row["country"] not in COUNTRIES:
            errs["country"] = "unknown_value"
    if "amount" in row:
        try:
            float(row["amount"])
        except Exception:
            errs["amount"] = "non_numeric"
    return (len(errs)==0), errs

def validate_df(df: pd.DataFrame):
    mask = []
    agg = {}
    for _, r in df.iterrows():
        ok, errs = row_is_valid(r)
        mask.append(ok)
        for k,v in errs.items():
            agg[f"{k}:{v}"] = agg.get(f"{k}:{v}", 0) + 1
    invalid = len(df) - sum(mask)
    criticality = "low" if invalid == 0 else ("high" if invalid == len(df) else "medium")
    return pd.Series(mask, index=df.index), agg, criticality
