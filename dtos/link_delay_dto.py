from pydantic import BaseModel
from datetime import datetime


class LinkDelayDTO(BaseModel):
    timebin: datetime
    asn: int
    magnitude: float
    asn_name: str

    class Config:
        from_attributes = True
