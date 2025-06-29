from sqlalchemy.orm import Session
from repositories.delay_repository import DelayRepository
from dtos.link_delay_dto import LinkDelayDTO
from typing import Optional, List, Tuple
from datetime import datetime


class LinkService:
    def __init__(self):
        self.delay_repository = DelayRepository()

    def get_link_delays(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        magnitude: Optional[float] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[LinkDelayDTO], int]:
        """
        Get link delay data with filtering.
        """
        delays, total_count = self.delay_repository.get_all(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            asn_ids=asn_ids,
            magnitude=magnitude,
            page=page,
            order_by=order_by
        )

        return [LinkDelayDTO(
            timebin=delay.timebin,
            asn=delay.asn,
            magnitude=delay.magnitude,
            asn_name=delay.asn_relation.name if delay.asn_relation else None
        ) for delay in delays], total_count
