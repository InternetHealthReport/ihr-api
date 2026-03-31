from datetime import datetime
from sqlalchemy.orm import Session, contains_eager, aliased
from sqlalchemy import select, func
from models.hegemony import Hegemony
from typing import Optional, List, Tuple
from utils import page_size


class HegemonyRepository:
    def get_all(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        originasn_ids: Optional[List[int]] = None,
        af: Optional[int] = None,
        hege: Optional[float] = None,
        hege_gte: Optional[float] = None,
        hege_lte: Optional[float] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[Hegemony], int]:
        ASN = aliased(Hegemony.asn_relation.property.mapper.class_)
        OriginASN = aliased(Hegemony.originasn_relation.property.mapper.class_)

        stmt = (
            select(Hegemony)
            .join(Hegemony.asn_relation.of_type(ASN))
            .join(Hegemony.originasn_relation.of_type(OriginASN))
            .options(
                contains_eager(Hegemony.asn_relation.of_type(ASN)),
                contains_eager(Hegemony.originasn_relation.of_type(OriginASN))
            )
        )

        if not timebin_gte and not timebin_lte:
            max_timebin = db.scalar(select(func.max(Hegemony.timebin)))
            stmt = stmt.where(Hegemony.timebin == max_timebin)

        if timebin_gte:
            stmt = stmt.where(Hegemony.timebin >= timebin_gte)
        if timebin_lte:
            stmt = stmt.where(Hegemony.timebin <= timebin_lte)
        if asn_ids:
            stmt = stmt.where(Hegemony.asn.in_(asn_ids))
        if originasn_ids:
            stmt = stmt.where(Hegemony.originasn.in_(originasn_ids))
        if af is not None:
            stmt = stmt.where(Hegemony.af == af)
        if hege is not None:
            stmt = stmt.where(Hegemony.hege == hege)
        if hege_gte:
            stmt = stmt.where(Hegemony.hege >= hege_gte)
        if hege_lte:
            stmt = stmt.where(Hegemony.hege <= hege_lte)

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        if order_by and hasattr(Hegemony, order_by):
            stmt = stmt.order_by(getattr(Hegemony, order_by))

        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).unique().all()

        return results, total_count
