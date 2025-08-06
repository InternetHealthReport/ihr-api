from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.hegemony_cone import HegemonyCone
from typing import Optional, List, Tuple
from utils import page_size
from sqlalchemy import func


class HegemonyConeRepository:
    def get_all(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        af: Optional[int] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[HegemonyCone], int]:
        query = db.query(HegemonyCone)

        # If no time filters specified, get rows with max timebin
        if not timebin_gte and not timebin_lte:
            max_timebin = db.query(func.max(HegemonyCone.timebin)).scalar()
            query = query.filter(HegemonyCone.timebin == max_timebin)
        
        # Apply filters
        if timebin_gte:
            query = query.filter(HegemonyCone.timebin >= timebin_gte)
        if timebin_lte:
            query = query.filter(HegemonyCone.timebin <= timebin_lte)
        if asn_ids:
            query = query.filter(HegemonyCone.asn.in_(asn_ids))
        if af:
            query = query.filter(HegemonyCone.af == af)

        total_count = query.count()

        # Apply ordering
        if order_by and hasattr(HegemonyCone, order_by):
            query = query.order_by(getattr(HegemonyCone, order_by))
        else:
            query = query.order_by(HegemonyCone.timebin)

        # Apply pagination
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
