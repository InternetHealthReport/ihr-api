from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.hegemony_cone import HegemonyCone
from typing import Optional, List, Tuple
from utils import page_size


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
        stmt = select(HegemonyCone)

        if not timebin_gte and not timebin_lte:
            max_timebin = db.scalar(select(func.max(HegemonyCone.timebin)))
            stmt = stmt.where(HegemonyCone.timebin == max_timebin)

        if timebin_gte:
            stmt = stmt.where(HegemonyCone.timebin >= timebin_gte)
        if timebin_lte:
            stmt = stmt.where(HegemonyCone.timebin <= timebin_lte)
        if asn_ids:
            stmt = stmt.where(HegemonyCone.asn.in_(asn_ids))
        if af:
            stmt = stmt.where(HegemonyCone.af == af)

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        if order_by and hasattr(HegemonyCone, order_by):
            stmt = stmt.order_by(getattr(HegemonyCone, order_by))
        else:
            stmt = stmt.order_by(HegemonyCone.timebin)

        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).all()

        return results, total_count
