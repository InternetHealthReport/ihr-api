from pydantic import BaseModel
from datetime import datetime


class HegemonyDTO(BaseModel):
    timebin: datetime
    originasn: int
    asn: int
    hege: float
    af: int
    asn_name: str
    originasn_name: str

    class Config:
        from_attributes = True
