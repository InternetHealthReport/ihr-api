from datetime import datetime
from sqlalchemy.orm import Session
from models.hegemony_alarms import HegemonyAlarms
from typing import Optional, List, Tuple
from globals import page_size


class HegemonyAlarmsRepository:
    def get_all(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        originasn_ids: Optional[List[int]] = None,
        af: Optional[int] = None,
        deviation_gte: Optional[float] = None,
        deviation_lte: Optional[float] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[HegemonyAlarms], int]:
        query = db.query(HegemonyAlarms)

        # Apply filters
        if timebin_gte:
            query = query.filter(HegemonyAlarms.timebin >= timebin_gte)
        if timebin_lte:
            query = query.filter(HegemonyAlarms.timebin <= timebin_lte)
        if asn_ids:
            query = query.filter(HegemonyAlarms.asn.in_(asn_ids))
        if originasn_ids:
            query = query.filter(
                HegemonyAlarms.originasn.in_(originasn_ids))
        if af is not None:
            query = query.filter(HegemonyAlarms.af == af)
        if deviation_gte:
            query = query.filter(HegemonyAlarms.deviation >= deviation_gte)
        if deviation_lte:
            query = query.filter(HegemonyAlarms.deviation <= deviation_lte)

        total_count = query.count()

        # Apply ordering
        if order_by and hasattr(HegemonyAlarms, order_by):
            query = query.order_by(getattr(HegemonyAlarms, order_by))

        # Apply pagination
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
