from sqlalchemy.orm import Session
from repositories.disco_events_repository import DiscoEventsRepository
from dtos.disco_events_dto import DiscoEventsDTO
from typing import List, Optional, Tuple
from datetime import datetime


class DiscoService:
    def __init__(self):
        self.disco_events_repository = DiscoEventsRepository()

    def get_disco_events(
        self,
        db: Session,
        streamname: Optional[str] = None,
        streamtype: Optional[str] = None,
        starttime: Optional[datetime] = None,
        starttime_gte: Optional[datetime] = None,
        starttime_lte: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
        endtime_gte: Optional[datetime] = None,
        endtime_lte: Optional[datetime] = None,
        avglevel: Optional[float] = None,
        avglevel_gte: Optional[float] = None,
        avglevel_lte: Optional[float] = None,
        nbdiscoprobes: Optional[int] = None,
        nbdiscoprobes_gte: Optional[int] = None,
        nbdiscoprobes_lte: Optional[int] = None,
        totalprobes: Optional[int] = None,
        totalprobes_gte: Optional[int] = None,
        totalprobes_lte: Optional[int] = None,
        ongoing: Optional[str] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[DiscoEventsDTO], int]:

        events_data, total_count = self.disco_events_repository.get_disco_events(
            db,
            streamname=streamname,
            streamtype=streamtype,
            starttime=starttime,
            starttime_gte=starttime_gte,
            starttime_lte=starttime_lte,
            endtime=endtime,
            endtime_gte=endtime_gte,
            endtime_lte=endtime_lte,
            avglevel=avglevel,
            avglevel_gte=avglevel_gte,
            avglevel_lte=avglevel_lte,
            nbdiscoprobes=nbdiscoprobes,
            nbdiscoprobes_gte=nbdiscoprobes_gte,
            nbdiscoprobes_lte=nbdiscoprobes_lte,
            totalprobes=totalprobes,
            totalprobes_gte=totalprobes_gte,
            totalprobes_lte=totalprobes_lte,
            ongoing=ongoing,
            page=page,
            order_by=order_by
        )

        return [DiscoEventsDTO.from_model(event) for event in events_data], total_count
