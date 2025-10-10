import pandas as pd
import pickle

# Load your pre-trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def predict(df: pd.DataFrame) -> pd.Series:
    """
    Make predictions using the trained Linear Regression model.
    """
    predictions = model.predict(df)
    return predictions
