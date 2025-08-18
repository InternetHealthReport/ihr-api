from datetime import datetime
from sqlalchemy.orm import Session
from models.metis_atlas_selection import MetisAtlasSelection
from typing import Optional, List, Tuple
from utils import page_size
from sqlalchemy import func


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
        query = db.query(MetisAtlasSelection).join(
            MetisAtlasSelection.asn_relation)

        # If no time filters specified, get rows with max timebin
        if not timebin and not timebin_gte and not timebin_lte:
            max_timebin = db.query(
                func.max(MetisAtlasSelection.timebin)).scalar()
            query = query.filter(MetisAtlasSelection.timebin == max_timebin)

        # Apply filters
        if timebin:
            query = query.filter(MetisAtlasSelection.timebin == timebin)
        if timebin_gte:
            query = query.filter(MetisAtlasSelection.timebin >= timebin_gte)
        if timebin_lte:
            query = query.filter(MetisAtlasSelection.timebin <= timebin_lte)
        if rank:
            query = query.filter(MetisAtlasSelection.rank == rank)
        if rank_lte:
            query = query.filter(MetisAtlasSelection.rank <= rank_lte)
        if rank_gte:
            query = query.filter(MetisAtlasSelection.rank >= rank_gte)
        if metric:
            query = query.filter(MetisAtlasSelection.metric == metric)
        if af:
            query = query.filter(MetisAtlasSelection.af == af)

        total_count = query.count()

        # Apply ordering
        if order_by and hasattr(MetisAtlasSelection, order_by):
            query = query.order_by(getattr(MetisAtlasSelection, order_by))

        # Apply pagination
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
