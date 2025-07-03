from datetime import datetime
from sqlalchemy.orm import Session
from models.forwarding import Forwarding
from typing import Optional, List, Tuple
from globals import page_size


class ForwardingRepository:
    def get_all(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        magnitude: Optional[float] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[Forwarding], int]:
        query = db.query(Forwarding).join(Forwarding.asn_relation)

        # Apply filters
        if timebin_gte:
            query = query.filter(Forwarding.timebin >= timebin_gte)
        if timebin_lte:
            query = query.filter(Forwarding.timebin <= timebin_lte)
        if asn_ids:
            query = query.filter(Forwarding.asn.in_(asn_ids))
        if magnitude is not None:
            query = query.filter(Forwarding.magnitude == magnitude)

        total_count = query.count()

        # Apply ordering
        if order_by and hasattr(Forwarding, order_by):
            query = query.order_by(getattr(Forwarding, order_by))
        else:
            query = query.order_by(Forwarding.timebin)

        # Apply pagination
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
