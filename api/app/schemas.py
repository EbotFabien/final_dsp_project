from pydantic import BaseModel

class HouseInput(BaseModel):
    squareMeters: float
    numberOfRooms: int
    hasYard: int
    hasPool: int
    floors: int
    cityCode: int
    cityPartRange: int
    numPrevOwners: int
    made: int
    isNewBuilt: int
    hasStormProtector: int
    basement: float
    attic: float
    garage: float
    hasStorageRoom: int
    hasGuestRoom: int
