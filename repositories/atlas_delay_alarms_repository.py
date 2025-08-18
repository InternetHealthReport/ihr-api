from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from models.atlas_delay_alarms import AtlasDelayAlarms
from datetime import datetime
from typing import List, Optional, Tuple
from utils import page_size
from sqlalchemy import func


class AtlasDelayAlarmsRepository:
    def get_alarms(
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
        startpoint_key: Optional[str] = None,
        endpoint_key: Optional[str] = None,
        deviation_gte: Optional[float] = None,
        deviation_lte: Optional[float] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[AtlasDelayAlarms], int]:
        """
        Get network delay alarms with all possible filters.
        """
        Startpoint = aliased(
            AtlasDelayAlarms.startpoint_relation.property.mapper.class_)
        Endpoint = aliased(
            AtlasDelayAlarms.endpoint_relation.property.mapper.class_)

        query = db.query(AtlasDelayAlarms)\
            .join(Startpoint, AtlasDelayAlarms.startpoint_relation)\
            .join(Endpoint, AtlasDelayAlarms.endpoint_relation)


        # If no time filters specified, get rows with max timebin
        if not timebin and not timebin_gte and not timebin_lte:
            max_timebin = db.query(func.max(AtlasDelayAlarms.timebin)).scalar()
            query = query.filter(AtlasDelayAlarms.timebin == max_timebin)
        
        if timebin:
            query = query.filter(AtlasDelayAlarms.timebin == timebin)
        if timebin_gte:
            query = query.filter(AtlasDelayAlarms.timebin >= timebin_gte)
        if timebin_lte:
            query = query.filter(AtlasDelayAlarms.timebin <= timebin_lte)

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

        if deviation_gte:
            query = query.filter(AtlasDelayAlarms.deviation >= deviation_gte)
        if deviation_lte:
            query = query.filter(AtlasDelayAlarms.deviation <= deviation_lte)

        total_count = query.count()

        if order_by and hasattr(AtlasDelayAlarms, order_by):
            query = query.order_by(getattr(AtlasDelayAlarms, order_by))

        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
