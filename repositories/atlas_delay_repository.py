from sqlalchemy.orm import Session, aliased, contains_eager
from sqlalchemy import select, func, and_, or_
from models.atlas_delay import AtlasDelay
from datetime import datetime
from typing import List, Optional, Tuple
from utils import page_size


class AtlasDelayRepository:
    def get_delays(
        self,
        db: Session,
        timebin: Optional[datetime] = None,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        startpoint_names: Optional[str] = None,
        endpoint_names: Optional[str] = None,
        startpoint_type: Optional[str] = None,
        endpoint_type: Optional[str] = None,
        startpoint_af: Optional[int] = None,
        endpoint_af: Optional[int] = None,
        median: Optional[float] = None,
        median_gte: Optional[float] = None,
        median_lte: Optional[float] = None,
        startpoint_key: Optional[str] = None,
        endpoint_key: Optional[str] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[AtlasDelay], int]:
        # Create SQLAlchemy aliases for the AtlasLocation table, used in both startpoint and endpoint
        # relationships. This is necessary because we are joining the same table (AtlasLocation) twice
        # in the query, and SQL requires different aliases for each instance to avoid ambiguity.
        Startpoint = aliased(AtlasDelay.startpoint_relation.property.mapper.class_)
        Endpoint = aliased(AtlasDelay.endpoint_relation.property.mapper.class_)

        stmt = (
            select(AtlasDelay)
            .join(AtlasDelay.startpoint_relation.of_type(Startpoint))
            .join(AtlasDelay.endpoint_relation.of_type(Endpoint))
            .options(
                contains_eager(AtlasDelay.startpoint_relation.of_type(Startpoint)),
                contains_eager(AtlasDelay.endpoint_relation.of_type(Endpoint))
            )
        )

        if not timebin and not timebin_gte and not timebin_lte:
            max_timebin = db.scalar(select(func.max(AtlasDelay.timebin)))
            stmt = stmt.where(AtlasDelay.timebin == max_timebin)

        if timebin:
            stmt = stmt.where(AtlasDelay.timebin == timebin)
        if timebin_gte:
            stmt = stmt.where(AtlasDelay.timebin >= timebin_gte)
        if timebin_lte:
            stmt = stmt.where(AtlasDelay.timebin <= timebin_lte)

        if startpoint_names:
            names = startpoint_names.split('|')
            stmt = stmt.where(Startpoint.name.in_(names))
        if startpoint_type:
            stmt = stmt.where(Startpoint.type == startpoint_type)
        if startpoint_af:
            stmt = stmt.where(Startpoint.af == startpoint_af)
        if startpoint_key:
            startpoint_conditions = []
            for key in startpoint_key.split('|'):
                if len(key) >= 2:
                    key_type = key[:2]
                    key_af = int(key[2]) if key[2].isdigit() else None
                    key_name = key[3:] if len(key) > 3 else None

                    conditions = []
                    if key_type:
                        conditions.append(Startpoint.type == key_type)
                    if key_af:
                        conditions.append(Startpoint.af == key_af)
                    if key_name:
                        conditions.append(Startpoint.name == key_name)

                    if conditions:
                        startpoint_conditions.append(and_(*conditions))

            if startpoint_conditions:
                stmt = stmt.where(or_(*startpoint_conditions))

        if endpoint_names:
            names = endpoint_names.split('|')
            stmt = stmt.where(Endpoint.name.in_(names))
        if endpoint_type:
            stmt = stmt.where(Endpoint.type == endpoint_type)
        if endpoint_af:
            stmt = stmt.where(Endpoint.af == endpoint_af)
        if endpoint_key:
            endpoint_conditions = []
            for key in endpoint_key.split('|'):
                if len(key) >= 2:
                    key_type = key[:2]
                    key_af = int(key[2]) if key[2].isdigit() else None
                    key_name = key[3:] if len(key) > 3 else None

                    conditions = []
                    if key_type:
                        conditions.append(Endpoint.type == key_type)
                    if key_af:
                        conditions.append(Endpoint.af == key_af)
                    if key_name:
                        conditions.append(Endpoint.name == key_name)

                    if conditions:
                        endpoint_conditions.append(and_(*conditions))

            if endpoint_conditions:
                stmt = stmt.where(or_(*endpoint_conditions))

        if median:
            stmt = stmt.where(AtlasDelay.median == median)
        if median_gte:
            stmt = stmt.where(AtlasDelay.median >= median_gte)
        if median_lte:
            stmt = stmt.where(AtlasDelay.median <= median_lte)

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        if order_by and hasattr(AtlasDelay, order_by):
            stmt = stmt.order_by(getattr(AtlasDelay, order_by))

        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).unique().all()

        return results, total_count
