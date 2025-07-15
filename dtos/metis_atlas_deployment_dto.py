from pydantic import BaseModel
from datetime import datetime


class MetisAtlasDeploymentDTO(BaseModel):
    timebin: datetime
    metric: str
    rank: int
    asn: int
    af: int
    nbsamples: int
    asn_name: str

    class Config:
        from_attributes = True
