from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MetisAtlasDeploymentDTO(BaseModel):
    timebin: datetime
    metric: str
    rank: int
    asn: int
    af: int
    nbsamples: int
    asn_name: str

    model_config = ConfigDict(from_attributes=True)
