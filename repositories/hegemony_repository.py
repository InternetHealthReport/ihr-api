from datetime import datetime
from sqlalchemy.orm import Session, contains_eager, aliased
from models.hegemony import Hegemony
from typing import Optional, List, Tuple
from utils import page_size
from sqlalchemy import func


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
        
        query = db.query(Hegemony)\
                .join(ASN, Hegemony.asn_relation)\
                .join(OriginASN, Hegemony.originasn_relation)\
                .options(   
                    contains_eager(Hegemony.asn_relation, alias=ASN),
                    contains_eager(Hegemony.originasn_relation, alias=OriginASN)
                )
        
        # If no time filters specified, get rows with max timebin
        if not timebin_gte and not timebin_lte:
            max_timebin = db.query(func.max(Hegemony.timebin)).scalar()
            query = query.filter(Hegemony.timebin == max_timebin)
        # Apply filters
        if timebin_gte:
            query = query.filter(Hegemony.timebin >= timebin_gte)
        if timebin_lte:
            query = query.filter(Hegemony.timebin <= timebin_lte)
        if asn_ids:
            query = query.filter(Hegemony.asn.in_(asn_ids))
        if originasn_ids:
            query = query.filter(Hegemony.originasn.in_(originasn_ids))
        if af is not None:
            query = query.filter(Hegemony.af == af)
        if hege is not None:
            query = query.filter(Hegemony.hege == hege)
        if hege_gte:
            query = query.filter(Hegemony.hege >= hege_gte)
        if hege_lte:
            query = query.filter(Hegemony.hege <= hege_lte)

        total_count = query.count()

        # Apply ordering
        if order_by and hasattr(Hegemony, order_by):
            query = query.order_by(getattr(Hegemony, order_by))

        # Apply pagination
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
