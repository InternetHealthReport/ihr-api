from pydantic import BaseModel
from datetime import datetime


class LinkForwardingDTO(BaseModel):
    timebin: datetime
    asn: int
    magnitude: float
    asn_name: str

    class Config:
        from_attributes = True
