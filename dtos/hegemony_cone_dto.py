from pydantic import BaseModel
from datetime import datetime


class HegemonyConeDTO(BaseModel):
    timebin: datetime
    asn: int
    conesize: int
    af: int

    class Config:
        from_attributes = True
