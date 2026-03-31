from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
