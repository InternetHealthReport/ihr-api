from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
