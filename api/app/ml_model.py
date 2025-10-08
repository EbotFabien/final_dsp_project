import pandas as pd

# Replace this with your actual trained ML model
def predict(df: pd.DataFrame) -> pd.Series:
    # Example mock prediction logic:
    return 1000 * df["numberOfRooms"] + 50 * df["squareMeters"]
