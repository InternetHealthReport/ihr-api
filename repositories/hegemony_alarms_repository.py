from datetime import datetime
from sqlalchemy.orm import Session, aliased, contains_eager
from sqlalchemy import select, func
from models.hegemony_alarms import HegemonyAlarms
from typing import Optional, List, Tuple
from utils import page_size


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
        ASN = aliased(HegemonyAlarms.asn_relation.property.mapper.class_)
        OriginASN = aliased(HegemonyAlarms.originasn_relation.property.mapper.class_)

        stmt = (
            select(HegemonyAlarms)
            .join(HegemonyAlarms.asn_relation.of_type(ASN))
            .join(HegemonyAlarms.originasn_relation.of_type(OriginASN))
            .options(
                contains_eager(HegemonyAlarms.asn_relation.of_type(ASN)),
                contains_eager(HegemonyAlarms.originasn_relation.of_type(OriginASN))
            )
        )

        # If no time filters specified, get rows with max timebin
        if not timebin_gte and not timebin_lte:
            max_timebin = db.scalar(select(func.max(HegemonyAlarms.timebin)))
            stmt = stmt.where(HegemonyAlarms.timebin == max_timebin)

        # Apply filters
        if timebin_gte:
            stmt = stmt.where(HegemonyAlarms.timebin >= timebin_gte)
        if timebin_lte:
            stmt = stmt.where(HegemonyAlarms.timebin <= timebin_lte)
        if asn_ids:
            stmt = stmt.where(HegemonyAlarms.asn.in_(asn_ids))
        if originasn_ids:
            stmt = stmt.where(HegemonyAlarms.originasn.in_(originasn_ids))
        if af is not None:
            stmt = stmt.where(HegemonyAlarms.af == af)
        if deviation_gte:
            stmt = stmt.where(HegemonyAlarms.deviation >= deviation_gte)
        if deviation_lte:
            stmt = stmt.where(HegemonyAlarms.deviation <= deviation_lte)

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        # Apply ordering
        if order_by and hasattr(HegemonyAlarms, order_by):
            stmt = stmt.order_by(getattr(HegemonyAlarms, order_by))

        # Apply pagination
        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).unique().all()

        return results, total_count
