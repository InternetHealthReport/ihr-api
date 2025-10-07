from datetime import datetime
from sqlalchemy.orm import Session, contains_eager, aliased
from models.hegemony_country import HegemonyCountry
from typing import Optional, List, Tuple
from utils import page_size
from sqlalchemy import func


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
        
        query = db.query(HegemonyCountry)\
                .join(ASN, HegemonyCountry.asn_relation)\
                .options(   
                    contains_eager(HegemonyCountry.asn_relation, alias=ASN),
                )

        # If no time filters specified, get rows with max timebin
        if not timebin_gte and not timebin_lte:
            max_timebin = db.query(func.max(HegemonyCountry.timebin)).scalar()
            query = query.filter(HegemonyCountry.timebin == max_timebin)

        # Apply filters
        if timebin_gte:
            query = query.filter(HegemonyCountry.timebin >= timebin_gte)
        if timebin_lte:
            query = query.filter(HegemonyCountry.timebin <= timebin_lte)
        if asn_ids:
            query = query.filter(HegemonyCountry.asn.in_(asn_ids))
        if countries:
            query = query.filter(HegemonyCountry.country.in_(countries))
        if af is not None:
            query = query.filter(HegemonyCountry.af == af)
        if weightscheme is not None:
            query = query.filter(HegemonyCountry.weightscheme == weightscheme)
        if transitonly is not None:
            query = query.filter(HegemonyCountry.transitonly == transitonly)
        if hege is not None:
            query = query.filter(HegemonyCountry.hege == hege)
        if hege_gte is not None:
            query = query.filter(HegemonyCountry.hege >= hege_gte)
        if hege_lte is not None:
            query = query.filter(HegemonyCountry.hege <= hege_lte)

        total_count = query.count()

        # Apply ordering
        if order_by and hasattr(HegemonyCountry, order_by):
            query = query.order_by(getattr(HegemonyCountry, order_by))

        # Apply pagination
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
