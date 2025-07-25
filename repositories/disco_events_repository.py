from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from models.disco_events import DiscoEvents
from datetime import datetime
from typing import List, Optional, Tuple
from utils import page_size


class DiscoEventsRepository:
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
    ) -> Tuple[List[DiscoEvents], int]:

        query = db.query(DiscoEvents)

        if streamname:
            query = query.filter(DiscoEvents.streamname == streamname)
        if streamtype:
            query = query.filter(DiscoEvents.streamtype == streamtype)

        if starttime:
            query = query.filter(DiscoEvents.starttime == starttime)
        if starttime_gte:
            query = query.filter(DiscoEvents.starttime >= starttime_gte)
        if starttime_lte:
            query = query.filter(DiscoEvents.starttime <= starttime_lte)

        if endtime:
            query = query.filter(DiscoEvents.endtime == endtime)
        if endtime_gte:
            query = query.filter(DiscoEvents.endtime >= endtime_gte)
        if endtime_lte:
            query = query.filter(DiscoEvents.endtime <= endtime_lte)

        if avglevel:
            query = query.filter(DiscoEvents.avglevel == avglevel)
        if avglevel_gte:
            query = query.filter(DiscoEvents.avglevel >= avglevel_gte)
        if avglevel_lte:
            query = query.filter(DiscoEvents.avglevel <= avglevel_lte)

        if nbdiscoprobes:
            query = query.filter(DiscoEvents.nbdiscoprobes == nbdiscoprobes)
        if nbdiscoprobes_gte:
            query = query.filter(
                DiscoEvents.nbdiscoprobes >= nbdiscoprobes_gte)
        if nbdiscoprobes_lte:
            query = query.filter(
                DiscoEvents.nbdiscoprobes <= nbdiscoprobes_lte)

        if totalprobes:
            query = query.filter(DiscoEvents.totalprobes == totalprobes)
        if totalprobes_gte:
            query = query.filter(DiscoEvents.totalprobes >= totalprobes_gte)
        if totalprobes_lte:
            query = query.filter(DiscoEvents.totalprobes <= totalprobes_lte)

        if ongoing:
            query = query.filter(DiscoEvents.ongoing == ongoing)

        total_count = query.count()

        if order_by and hasattr(DiscoEvents, order_by):
            query = query.order_by(getattr(DiscoEvents, order_by))

        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
