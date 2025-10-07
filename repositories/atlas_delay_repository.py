from sqlalchemy.orm import Session, aliased, contains_eager
from sqlalchemy import and_, or_
from models.atlas_delay import AtlasDelay
from datetime import datetime
from typing import List, Optional, Tuple
from utils import page_size
from sqlalchemy import func


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
        """
        Get network delays with all possible filters.
        """
        # Create SQLAlchemy aliases for the AtlasLocation table, used in both startpoint and endpoint relationships.
        # This is necessary because we are joining the same table (AtlasLocation) twice in the query,
        # and SQL requires different aliases for each instance to avoid ambiguity.
        Startpoint = aliased(
            AtlasDelay.startpoint_relation.property.mapper.class_)
        Endpoint = aliased(AtlasDelay.endpoint_relation.property.mapper.class_)

        query = db.query(AtlasDelay)\
            .join(Startpoint, AtlasDelay.startpoint_relation)\
            .join(Endpoint, AtlasDelay.endpoint_relation)\
            .options(   
                    contains_eager(AtlasDelay.startpoint_relation, alias=Startpoint),
                    contains_eager(AtlasDelay.endpoint_relation, alias=Endpoint)
                )


        # If no time filters specified, get rows with max timebin
        if not timebin and not timebin_gte and not timebin_lte:
            max_timebin = db.query(func.max(AtlasDelay.timebin)).scalar()
            query = query.filter(AtlasDelay.timebin == max_timebin)
        
        # Apply timebin filters
        if timebin:
            query = query.filter(AtlasDelay.timebin == timebin)
        if timebin_gte:
            query = query.filter(AtlasDelay.timebin >= timebin_gte)
        if timebin_lte:
            query = query.filter(AtlasDelay.timebin <= timebin_lte)

        if startpoint_names:
            names = startpoint_names.split('|')
            query = query.filter(Startpoint.name.in_(names))
        if startpoint_type:
            query = query.filter(Startpoint.type == startpoint_type)
        if startpoint_af:
            query = query.filter(Startpoint.af == startpoint_af)
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
                query = query.filter(or_(*startpoint_conditions))

        if endpoint_names:
            names = endpoint_names.split('|')
            query = query.filter(Endpoint.name.in_(names))
        if endpoint_type:
            query = query.filter(Endpoint.type == endpoint_type)
        if endpoint_af:
            query = query.filter(Endpoint.af == endpoint_af)
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
                query = query.filter(or_(*endpoint_conditions))

        if median:
            query = query.filter(AtlasDelay.median == median)
        if median_gte:
            query = query.filter(AtlasDelay.median >= median_gte)
        if median_lte:
            query = query.filter(AtlasDelay.median <= median_lte)

        total_count = query.count()

        # Apply ordering
        if order_by and hasattr(AtlasDelay, order_by):
            query = query.order_by(getattr(AtlasDelay, order_by))

        # Apply pagination
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
