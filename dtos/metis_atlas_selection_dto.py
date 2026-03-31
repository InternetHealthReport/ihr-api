from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MetisAtlasSelectionDTO(BaseModel):
    timebin: datetime
    metric: str
    rank: int
    asn: int
    af: int
    asn_name: str

    model_config = ConfigDict(from_attributes=True)
