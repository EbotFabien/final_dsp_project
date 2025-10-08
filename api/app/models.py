from sqlalchemy import Column, Integer, Float, String
from .database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    squareMeters = Column(Float)
    numberOfRooms = Column(Integer)
    hasYard = Column(Integer)
    hasPool = Column(Integer)
    floors = Column(Integer)
    cityCode = Column(Integer)
    cityPartRange = Column(Integer)
    numPrevOwners = Column(Integer)
    made = Column(Integer)
    isNewBuilt = Column(Integer)
    hasStormProtector = Column(Integer)
    basement = Column(Float)
    attic = Column(Float)
    garage = Column(Float)
    hasStorageRoom = Column(Integer)
    hasGuestRoom = Column(Integer)
    price = Column(Float)
    source = Column(String, default="webapp")  # webapp or scheduled job
