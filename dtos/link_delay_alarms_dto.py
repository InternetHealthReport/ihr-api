from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class LinkDelayAlarmsDTO(BaseModel):
    timebin: datetime
    asn: int
    asn_name: Optional[str]
    link: str
    medianrtt: float
    diffmedian: float
    deviation: float
    nbprobes: int
    msm_prb_ids: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True
