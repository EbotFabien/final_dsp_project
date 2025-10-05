from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, func
from .database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    input_features = Column(JSON, nullable=False)
    prediction = Column(Float, nullable=False)
    model_name = Column(String, default="example_model")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
