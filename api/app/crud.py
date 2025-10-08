from sqlalchemy.orm import Session
from models import Prediction

def save_prediction(db: Session, prediction: dict, source: str = "webapp"):
    db_pred = Prediction(**prediction, source=source)
    db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred

def get_predictions(db: Session, start_date=None, end_date=None, source="all"):
    query = db.query(Prediction)
    if source != "all":
        query = query.filter(Prediction.source == source)
    # You can add date filtering if you add a created_at column
    return query.all()
