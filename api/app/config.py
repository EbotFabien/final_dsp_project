# config.py
import os

# PostgreSQL connection URL
# Format: postgresql://username:password@host:port/dbname
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/housing_predictions"
)

# ML model path
MODEL_PATH = os.getenv("MODEL_PATH", "./models/house_price_model.pkl")

# API title
API_TITLE = "House Price Prediction API"
