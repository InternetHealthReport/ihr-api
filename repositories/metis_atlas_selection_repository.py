from datetime import datetime
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy import select, func
from models.metis_atlas_selection import MetisAtlasSelection
from typing import Optional, List, Tuple
from utils import page_size


class MetisAtlasSelectionRepository:
    def get_all(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        timebin: Optional[datetime] = None,
        rank: Optional[int] = None,
        rank_lte: Optional[int] = None,
        rank_gte: Optional[int] = None,
        metric: Optional[str] = None,
        af: Optional[int] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[MetisAtlasSelection], int]:
        stmt = (
            select(MetisAtlasSelection)
            .join(MetisAtlasSelection.asn_relation)
            .options(contains_eager(MetisAtlasSelection.asn_relation))
        )

        if not timebin and not timebin_gte and not timebin_lte:
            max_timebin = db.scalar(select(func.max(MetisAtlasSelection.timebin)))
            stmt = stmt.where(MetisAtlasSelection.timebin == max_timebin)

        if timebin:
            stmt = stmt.where(MetisAtlasSelection.timebin == timebin)
        if timebin_gte:
            stmt = stmt.where(MetisAtlasSelection.timebin >= timebin_gte)
        if timebin_lte:
            stmt = stmt.where(MetisAtlasSelection.timebin <= timebin_lte)
        if rank:
            stmt = stmt.where(MetisAtlasSelection.rank == rank)
        if rank_lte:
            stmt = stmt.where(MetisAtlasSelection.rank <= rank_lte)
        if rank_gte:
            stmt = stmt.where(MetisAtlasSelection.rank >= rank_gte)
        if metric:
            stmt = stmt.where(MetisAtlasSelection.metric == metric)
        if af:
            stmt = stmt.where(MetisAtlasSelection.af == af)

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        if order_by and hasattr(MetisAtlasSelection, order_by):
            stmt = stmt.order_by(getattr(MetisAtlasSelection, order_by))

        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).unique().all()

        return results, total_count
