from datetime import datetime
from sqlalchemy.orm import Session, contains_eager, aliased
from sqlalchemy import select, func
from models.hegemony_prefix import HegemonyPrefix
from typing import Optional, List, Tuple
from utils import page_size


class HegemonyPrefixRepository:
    def get_all(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        prefixes: Optional[List[str]] = None,
        asn_ids: Optional[List[int]] = None,
        originasn_ids: Optional[List[int]] = None,
        countries: Optional[List[str]] = None,
        rpki_status: Optional[str] = None,
        irr_status: Optional[str] = None,
        delegated_prefix_status: Optional[str] = None,
        delegated_asn_status: Optional[str] = None,
        af: Optional[int] = None,
        hege: Optional[float] = None,
        hege_gte: Optional[float] = None,
        hege_lte: Optional[float] = None,
        origin_only: Optional[bool] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[HegemonyPrefix], int]:
        ASN = aliased(HegemonyPrefix.asn_relation.property.mapper.class_)
        OriginASN = aliased(HegemonyPrefix.originasn_relation.property.mapper.class_)

        stmt = (
            select(HegemonyPrefix)
            .join(HegemonyPrefix.asn_relation.of_type(ASN))
            .join(HegemonyPrefix.originasn_relation.of_type(OriginASN))
            .options(
                contains_eager(HegemonyPrefix.asn_relation.of_type(ASN)),
                contains_eager(HegemonyPrefix.originasn_relation.of_type(OriginASN))
            )
        )

        # If no time filters specified, get rows with max timebin
        if not timebin_gte and not timebin_lte:
            max_timebin = db.scalar(select(func.max(HegemonyPrefix.timebin)))
            stmt = stmt.where(HegemonyPrefix.timebin == max_timebin)

        # Apply filters
        if timebin_gte:
            stmt = stmt.where(HegemonyPrefix.timebin >= timebin_gte)
        if timebin_lte:
            stmt = stmt.where(HegemonyPrefix.timebin <= timebin_lte)
        if prefixes:
            stmt = stmt.where(HegemonyPrefix.prefix.in_(prefixes))
        if asn_ids:
            stmt = stmt.where(HegemonyPrefix.asn.in_(asn_ids))
        if originasn_ids:
            stmt = stmt.where(HegemonyPrefix.originasn.in_(originasn_ids))
        if countries:
            stmt = stmt.where(HegemonyPrefix.country.in_(countries))
        if rpki_status:
            stmt = stmt.where(HegemonyPrefix.rpki_status.contains(rpki_status))
        if irr_status:
            stmt = stmt.where(HegemonyPrefix.irr_status.contains(irr_status))
        if delegated_prefix_status:
            stmt = stmt.where(HegemonyPrefix.delegated_prefix_status.contains(delegated_prefix_status))
        if delegated_asn_status:
            stmt = stmt.where(HegemonyPrefix.delegated_asn_status.contains(delegated_asn_status))
        if af is not None:
            stmt = stmt.where(HegemonyPrefix.af == af)
        if hege is not None:
            stmt = stmt.where(HegemonyPrefix.hege == hege)
        if hege_gte is not None:
            stmt = stmt.where(HegemonyPrefix.hege >= hege_gte)
        if hege_lte is not None:
            stmt = stmt.where(HegemonyPrefix.hege <= hege_lte)
        if origin_only:
            stmt = stmt.where(HegemonyPrefix.originasn == HegemonyPrefix.asn)

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        # Apply ordering
        if order_by and hasattr(HegemonyPrefix, order_by):
            stmt = stmt.order_by(getattr(HegemonyPrefix, order_by))

        # Apply pagination
        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).unique().all()

        return results, total_count
