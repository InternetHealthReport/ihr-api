from dtos.disco_probes_dto import DiscoProbesDTO
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class DiscoEventsDTO(BaseModel):
    id: int
    streamtype: str
    streamname: str
    starttime: datetime
    endtime: datetime
    avglevel: float
    nbdiscoprobes: int
    totalprobes: int
    ongoing: bool
    discoprobes: Optional[List[DiscoProbesDTO]] = None

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_model(disco_event, include_probe_details: bool = False):
        return DiscoEventsDTO(
            id=disco_event.id,
            streamtype=disco_event.streamtype,
            streamname=disco_event.streamname,
            starttime=disco_event.starttime,
            endtime=disco_event.endtime,
            avglevel=disco_event.avglevel,
            nbdiscoprobes=disco_event.nbdiscoprobes,
            totalprobes=disco_event.totalprobes,
            ongoing=disco_event.ongoing,
            discoprobes=[DiscoProbesDTO.model_validate(probe) for probe in disco_event.probes]
            if include_probe_details else None,
        )
