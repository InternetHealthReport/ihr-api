from sqlalchemy.orm import Session
from repositories.hegemony_cone_repository import HegemonyConeRepository
from dtos.hegemony_cone_dto import HegemonyConeDTO
from typing import Optional, List, Tuple
from datetime import datetime


class HegemonyConeService:
    def __init__(self):
        self.repository = HegemonyConeRepository()

    def get_hegemony_cones(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        af: Optional[int] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[HegemonyConeDTO], int]:
        """
        Get hegemony cone data with time-based filtering.
        """
        cones, total_count = self.repository.get_all(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            asn_ids=asn_ids,
            af=af,
            page=page,
            order_by=order_by
        )

        return [HegemonyConeDTO(
            timebin=cone.timebin,
            asn=cone.asn,
            conesize=cone.conesize,
            af=cone.af
        ) for cone in cones], total_count
