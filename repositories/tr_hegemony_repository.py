from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from models.tr_hegemony import TRHegemony
from datetime import datetime
from typing import List, Optional, Tuple
from utils import page_size
from sqlalchemy import func


class TRHegemonyRepository:
    def get_tr_hegemony(
        self,
        db: Session,
        timebin: Optional[datetime] = None,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        origin_names: Optional[str] = None,
        dependency_names: Optional[str] = None,
        origin_type: Optional[str] = None,
        dependency_type: Optional[str] = None,
        origin_af: Optional[int] = None,
        dependency_af: Optional[int] = None,
        hege: Optional[float] = None,
        hege_gte: Optional[float] = None,
        hege_lte: Optional[float] = None,
        af: Optional[int] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[TRHegemony], int]:

        Origin = aliased(TRHegemony.origin_relation.property.mapper.class_)
        Dependency = aliased(
            TRHegemony.dependency_relation.property.mapper.class_)

        query = db.query(TRHegemony)\
            .join(Origin, TRHegemony.origin_relation)\
            .join(Dependency, TRHegemony.dependency_relation)

        # If no time filters specified, get rows with max timebin
        if not timebin and not timebin_gte and not timebin_lte:
            max_timebin = db.query(func.max(TRHegemony.timebin)).scalar()
            query = query.filter(TRHegemony.timebin == max_timebin)
        
        if timebin:
            query = query.filter(TRHegemony.timebin == timebin)
        if timebin_gte:
            query = query.filter(TRHegemony.timebin >= timebin_gte)
        if timebin_lte:
            query = query.filter(TRHegemony.timebin <= timebin_lte)

        if origin_names:
            names = origin_names.split('|')
            query = query.filter(Origin.name.in_(names))
        if origin_type:
            query = query.filter(Origin.type == origin_type)
        if origin_af:
            query = query.filter(Origin.af == origin_af)

        if dependency_names:
            names = dependency_names.split('|')
            query = query.filter(Dependency.name.in_(names))
        if dependency_type:
            query = query.filter(Dependency.type == dependency_type)
        if dependency_af:
            query = query.filter(Dependency.af == dependency_af)

        if hege:
            query = query.filter(TRHegemony.hege == hege)
        if hege_gte:
            query = query.filter(TRHegemony.hege >= hege_gte)
        if hege_lte:
            query = query.filter(TRHegemony.hege <= hege_lte)

        if af:
            query = query.filter(TRHegemony.af == af)

        total_count = query.count()

        if order_by and hasattr(TRHegemony, order_by):
            query = query.order_by(getattr(TRHegemony, order_by))

        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
