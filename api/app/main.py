from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from . import crud, models, schemas, ml_model

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Model Prediction API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/predict", response_model=schemas.PredictionResponse)
def predict(request: schemas.PredictionRequest, db: Session = Depends(get_db)):
    predictions = ml_model.make_predictions(request.features)
    crud.save_predictions(db, request.features, predictions)
    return {"predictions": predictions}

@app.get("/past-predictions", response_model=list[schemas.PastPredictionResponse])
def past_predictions(db: Session = Depends(get_db)):
    records = crud.get_past_predictions(db)
    return records
