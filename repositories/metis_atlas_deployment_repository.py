from datetime import datetime
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy import select, func
from models.metis_atlas_deployment import MetisAtlasDeployment
from typing import Optional, List, Tuple
from utils import page_size


class MetisAtlasDeploymentRepository:
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
    ) -> Tuple[List[MetisAtlasDeployment], int]:
        stmt = (
            select(MetisAtlasDeployment)
            .join(MetisAtlasDeployment.asn_relation)
            .options(contains_eager(MetisAtlasDeployment.asn_relation))
        )

        if not timebin and not timebin_gte and not timebin_lte:
            max_timebin = db.scalar(select(func.max(MetisAtlasDeployment.timebin)))
            stmt = stmt.where(MetisAtlasDeployment.timebin == max_timebin)

        if timebin:
            stmt = stmt.where(MetisAtlasDeployment.timebin == timebin)
        if timebin_gte:
            stmt = stmt.where(MetisAtlasDeployment.timebin >= timebin_gte)
        if timebin_lte:
            stmt = stmt.where(MetisAtlasDeployment.timebin <= timebin_lte)
        if rank:
            stmt = stmt.where(MetisAtlasDeployment.rank == rank)
        if rank_lte:
            stmt = stmt.where(MetisAtlasDeployment.rank <= rank_lte)
        if rank_gte:
            stmt = stmt.where(MetisAtlasDeployment.rank >= rank_gte)
        if metric:
            stmt = stmt.where(MetisAtlasDeployment.metric == metric)
        if af:
            stmt = stmt.where(MetisAtlasDeployment.af == af)

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        if order_by and hasattr(MetisAtlasDeployment, order_by):
            stmt = stmt.order_by(getattr(MetisAtlasDeployment, order_by))

        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).unique().all()

        return results, total_count
