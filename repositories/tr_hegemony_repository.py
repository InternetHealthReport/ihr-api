from sqlalchemy.orm import Session, aliased, contains_eager
from sqlalchemy import select, func, and_, or_
from models.tr_hegemony import TRHegemony
from datetime import datetime
from typing import List, Optional, Tuple
from utils import page_size


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
        Dependency = aliased(TRHegemony.dependency_relation.property.mapper.class_)

        stmt = (
            select(TRHegemony)
            .join(TRHegemony.origin_relation.of_type(Origin))
            .join(TRHegemony.dependency_relation.of_type(Dependency))
            .options(
                contains_eager(TRHegemony.origin_relation.of_type(Origin)),
                contains_eager(TRHegemony.dependency_relation.of_type(Dependency))
            )
        )

        # If no time filters specified, get rows with max timebin
        if not timebin and not timebin_gte and not timebin_lte:
            max_timebin = db.scalar(select(func.max(TRHegemony.timebin)))
            stmt = stmt.where(TRHegemony.timebin == max_timebin)

        if timebin:
            stmt = stmt.where(TRHegemony.timebin == timebin)
        if timebin_gte:
            stmt = stmt.where(TRHegemony.timebin >= timebin_gte)
        if timebin_lte:
            stmt = stmt.where(TRHegemony.timebin <= timebin_lte)

        if origin_names:
            names = origin_names.split('|')
            stmt = stmt.where(Origin.name.in_(names))
        if origin_type:
            stmt = stmt.where(Origin.type == origin_type)
        if origin_af:
            stmt = stmt.where(Origin.af == origin_af)

        if dependency_names:
            names = dependency_names.split('|')
            stmt = stmt.where(Dependency.name.in_(names))
        if dependency_type:
            stmt = stmt.where(Dependency.type == dependency_type)
        if dependency_af:
            stmt = stmt.where(Dependency.af == dependency_af)

        if hege:
            stmt = stmt.where(TRHegemony.hege == hege)
        if hege_gte:
            stmt = stmt.where(TRHegemony.hege >= hege_gte)
        if hege_lte:
            stmt = stmt.where(TRHegemony.hege <= hege_lte)
        if af:
            stmt = stmt.where(TRHegemony.af == af)

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        if order_by and hasattr(TRHegemony, order_by):
            stmt = stmt.order_by(getattr(TRHegemony, order_by))

        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).unique().all()

        return results, total_count
