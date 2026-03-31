from datetime import datetime
from sqlalchemy.orm import Session, contains_eager, aliased
from sqlalchemy import select, func
from models.hegemony_country import HegemonyCountry
from typing import Optional, List, Tuple
from utils import page_size


class HegemonyCountryRepository:
    def get_all(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        countries: Optional[List[str]] = None,
        af: Optional[int] = None,
        weightscheme: Optional[str] = None,
        transitonly: Optional[bool] = None,
        hege: Optional[float] = None,
        hege_gte: Optional[float] = None,
        hege_lte: Optional[float] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[HegemonyCountry], int]:
        ASN = aliased(HegemonyCountry.asn_relation.property.mapper.class_)

        stmt = (
            select(HegemonyCountry)
            .join(HegemonyCountry.asn_relation.of_type(ASN))
            .options(contains_eager(HegemonyCountry.asn_relation.of_type(ASN)))
        )

        if not timebin_gte and not timebin_lte:
            max_timebin = db.scalar(select(func.max(HegemonyCountry.timebin)))
            stmt = stmt.where(HegemonyCountry.timebin == max_timebin)

        if timebin_gte:
            stmt = stmt.where(HegemonyCountry.timebin >= timebin_gte)
        if timebin_lte:
            stmt = stmt.where(HegemonyCountry.timebin <= timebin_lte)
        if asn_ids:
            stmt = stmt.where(HegemonyCountry.asn.in_(asn_ids))
        if countries:
            stmt = stmt.where(HegemonyCountry.country.in_(countries))
        if af is not None:
            stmt = stmt.where(HegemonyCountry.af == af)
        if weightscheme is not None:
            stmt = stmt.where(HegemonyCountry.weightscheme == weightscheme)
        if transitonly is not None:
            stmt = stmt.where(HegemonyCountry.transitonly == transitonly)
        if hege is not None:
            stmt = stmt.where(HegemonyCountry.hege == hege)
        if hege_gte is not None:
            stmt = stmt.where(HegemonyCountry.hege >= hege_gte)
        if hege_lte is not None:
            stmt = stmt.where(HegemonyCountry.hege <= hege_lte)

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        if order_by and hasattr(HegemonyCountry, order_by):
            stmt = stmt.order_by(getattr(HegemonyCountry, order_by))

        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).unique().all()

        return results, total_count
