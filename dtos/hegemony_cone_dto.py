from pydantic import BaseModel, ConfigDict
from datetime import datetime


class HegemonyConeDTO(BaseModel):
    timebin: datetime
    asn: int
    conesize: int
    af: int

    model_config = ConfigDict(from_attributes=True)
