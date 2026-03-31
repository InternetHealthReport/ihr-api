from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DiscoProbesDTO(BaseModel):
    probe_id: int
    starttime: datetime
    endtime: datetime
    level: float
    ipv4: str
    prefixv4: str
    event: int
    lat: float
    lon: float

    model_config = ConfigDict(from_attributes=True)
