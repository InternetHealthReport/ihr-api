from pydantic import BaseModel
from datetime import datetime


class MetisAtlasSelectionDTO(BaseModel):
    timebin: datetime
    metric: str
    rank: int
    asn: int
    af: int
    asn_name: str

    class Config:
        from_attributes = True
