from datetime import datetime
from sqlalchemy.orm import Session, contains_eager, aliased
from models.hegemony_prefix import HegemonyPrefix
from typing import Optional, List, Tuple
from utils import page_size
from sqlalchemy import func


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
        
        query = db.query(HegemonyPrefix)\
                .join(ASN, HegemonyPrefix.asn_relation)\
                .join(OriginASN, HegemonyPrefix.originasn_relation)\
                .options(   
                    contains_eager(HegemonyPrefix.asn_relation, alias=ASN),
                    contains_eager(HegemonyPrefix.originasn_relation, alias=OriginASN)
                )
        # If no time filters specified, get rows with max timebin
        if not timebin_gte and not timebin_lte:
            max_timebin = db.query(func.max(HegemonyPrefix.timebin)).scalar()
            query = query.filter(HegemonyPrefix.timebin == max_timebin)

        # Apply filters
        if timebin_gte:
            query = query.filter(HegemonyPrefix.timebin >= timebin_gte)
        if timebin_lte:
            query = query.filter(HegemonyPrefix.timebin <= timebin_lte)
        if prefixes:
            query = query.filter(HegemonyPrefix.prefix.in_(prefixes))
        if asn_ids:
            query = query.filter(HegemonyPrefix.asn.in_(asn_ids))
        if originasn_ids:
            query = query.filter(HegemonyPrefix.originasn.in_(originasn_ids))
        if countries:
            query = query.filter(HegemonyPrefix.country.in_(countries))
        if rpki_status:
            query = query.filter(
                HegemonyPrefix.rpki_status.contains(rpki_status))
        if irr_status:
            query = query.filter(
                HegemonyPrefix.irr_status.contains(irr_status))
        if delegated_prefix_status:
            query = query.filter(
                HegemonyPrefix.delegated_prefix_status.contains(delegated_prefix_status))
        if delegated_asn_status:
            query = query.filter(
                HegemonyPrefix.delegated_asn_status.contains(delegated_asn_status))
        if af is not None:
            query = query.filter(HegemonyPrefix.af == af)
        if hege is not None:
            query = query.filter(HegemonyPrefix.hege == hege)
        if hege_gte is not None:
            query = query.filter(HegemonyPrefix.hege >= hege_gte)
        if hege_lte is not None:
            query = query.filter(HegemonyPrefix.hege <= hege_lte)
        if origin_only:
            query = query.filter(
                HegemonyPrefix.originasn == HegemonyPrefix.asn)

        total_count = query.count()

        # Apply ordering
        if order_by and hasattr(HegemonyPrefix, order_by):
            query = query.order_by(getattr(HegemonyPrefix, order_by))

        # Apply pagination
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
