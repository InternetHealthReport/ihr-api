from pydantic import BaseModel, ConfigDict
from datetime import datetime


class HegemonyDTO(BaseModel):
    timebin: datetime
    originasn: int
    asn: int
    hege: float
    af: int
    asn_name: str
    originasn_name: str

    model_config = ConfigDict(from_attributes=True)
