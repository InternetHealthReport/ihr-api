from pydantic import BaseModel
from datetime import datetime


class HegemonyCountryDTO(BaseModel):
    timebin: datetime
    country: str
    asn: int
    hege: float
    af: int
    asn_name: str
    weight: float
    weightscheme: str
    transitonly: bool

    class Config:
        from_attributes = True
