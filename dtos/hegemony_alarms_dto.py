from pydantic import BaseModel
from datetime import datetime


class HegemonyAlarmsDTO(BaseModel):
    timebin: datetime
    originasn: int
    asn: int
    deviation: float
    af: int
    asn_name: str
    originasn_name: str

    class Config:
        from_attributes = True
