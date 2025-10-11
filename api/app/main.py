from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas import HouseInput
from ml_model import predict
from database import SessionLocal, engine, Base
from crud import save_prediction, get_predictions
import pandas as pd
from typing import List
from fastapi import Query

# Create tables
Base.metadata.create_all(bind=engine)



app = FastAPI(title="House Price Prediction API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/predict_single/")
def predict_single(input_data: HouseInput, db: Session = Depends(get_db)):
    df = pd.DataFrame([input_data.dict()])
    prediction = predict(df)
    df["price"] = prediction
    # Save prediction to DB
    save_prediction(db, df.to_dict(orient="records")[0], source="webapp")
    return df.to_dict(orient="records")[0]

@app.post("/predict_batch/")
def predict_batch(inputs: List[HouseInput],source: str = Query("webapp"),db: Session = Depends(get_db)):
    # Convert all input dicts into a DataFrame
    df = pd.DataFrame([i.dict() for i in inputs])

    # Make batch predictions
    predictions = predict(df)
    df["price"] = predictions

    # Save each prediction to the DB
    for record in df.to_dict(orient="records"):
        save_prediction(db, record, source="webapp")

    # Return all results as JSON
    return {"predictions": df.to_dict(orient="records")}



@app.get("/past-predictions/")
def past_predictions(source: str = "all", db: Session = Depends(get_db)):
    """
    Retrieve past predictions from the DB.
    source: "webapp", "scheduled", or "all"
    """
    preds = get_predictions(db, source=source)
    # Convert SQLAlchemy objects to dicts
    return [vars(p) for p in preds]
