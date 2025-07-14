from datetime import datetime
from sqlalchemy.orm import Session
from models.delay_alarms import DelayAlarms
from typing import Optional, List, Tuple
from globals import page_size


class DelayAlarmsRepository:
    def get_all(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        deviation_gte: Optional[float] = None,
        deviation_lte: Optional[float] = None,
        diffmedian_gte: Optional[float] = None,
        diffmedian_lte: Optional[float] = None,
        medianrtt_gte: Optional[float] = None,
        medianrtt_lte: Optional[float] = None,
        nbprobes_gte: Optional[int] = None,
        nbprobes_lte: Optional[int] = None,
        link: Optional[str] = None,
        link_contains: Optional[str] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[DelayAlarms], int]:
        query = db.query(DelayAlarms).join(DelayAlarms.asn_relation)

        # Apply filters
        if timebin_gte:
            query = query.filter(DelayAlarms.timebin >= timebin_gte)
        if timebin_lte:
            query = query.filter(DelayAlarms.timebin <= timebin_lte)
        if asn_ids:
            query = query.filter(DelayAlarms.asn.in_(asn_ids))
        if deviation_gte:
            query = query.filter(DelayAlarms.deviation >= deviation_gte)
        if deviation_lte:
            query = query.filter(DelayAlarms.deviation <= deviation_lte)
        if diffmedian_gte:
            query = query.filter(DelayAlarms.diffmedian >= diffmedian_gte)
        if diffmedian_lte:
            query = query.filter(DelayAlarms.diffmedian <= diffmedian_lte)
        if medianrtt_gte:
            query = query.filter(DelayAlarms.medianrtt >= medianrtt_gte)
        if medianrtt_lte:
            query = query.filter(DelayAlarms.medianrtt <= medianrtt_lte)
        if nbprobes_gte:
            query = query.filter(DelayAlarms.nbprobes >= nbprobes_gte)
        if nbprobes_lte:
            query = query.filter(DelayAlarms.nbprobes <= nbprobes_lte)
        if link:
            query = query.filter(DelayAlarms.link == link)
        if link_contains:
            query = query.filter(DelayAlarms.link.contains(link_contains))

        total_count = query.count()

        # Apply ordering
        if order_by and hasattr(DelayAlarms, order_by.replace('-', '')):
            if order_by.startswith('-'):
                query = query.order_by(
                    getattr(DelayAlarms, order_by[1:]).desc())
            else:
                query = query.order_by(getattr(DelayAlarms, order_by))
        else:
            query = query.order_by(DelayAlarms.timebin.desc())

        # Apply pagination
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
