from pydantic import BaseModel
from datetime import datetime


class HegemonyPrefixDTO(BaseModel):
    timebin: datetime
    prefix: str
    originasn: int
    country: str
    asn: int
    hege: float
    af: int
    visibility: float
    rpki_status: str
    irr_status: str
    delegated_prefix_status: str
    delegated_asn_status: str
    descr: str
    moas: bool
    originasn_name: str
    asn_name: str

    class Config:
        from_attributes = True
