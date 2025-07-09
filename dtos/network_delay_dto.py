from pydantic import BaseModel
from datetime import datetime


class NetworkDelayDTO(BaseModel):
    timebin: datetime
    startpoint_type: str
    startpoint_name: str
    startpoint_af: int
    endpoint_type: str
    endpoint_name: str
    endpoint_af: int
    median: float
    nbtracks: int
    nbprobes: int
    entropy: float
    hop: int
    nbrealrtts: int

    class Config:
        from_attributes = True

    @staticmethod
    def from_model(atlasDelay):
        return NetworkDelayDTO(
            timebin=atlasDelay.timebin,
            startpoint_type=atlasDelay.startpoint_relation.type,
            startpoint_name=atlasDelay.startpoint_relation.name,
            startpoint_af=atlasDelay.startpoint_relation.af,
            endpoint_type=atlasDelay.endpoint_relation.type,
            endpoint_name=atlasDelay.endpoint_relation.name,
            endpoint_af=atlasDelay.endpoint_relation.af,
            median=atlasDelay.median,
            nbtracks=atlasDelay.nbtracks,
            nbprobes=atlasDelay.nbprobes,
            entropy=atlasDelay.entropy,
            hop=atlasDelay.hop,
            nbrealrtts=atlasDelay.nbrealrtts,
        )
