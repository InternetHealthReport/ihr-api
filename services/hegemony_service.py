from sqlalchemy.orm import Session
from repositories.hegemony_cone_repository import HegemonyConeRepository
from dtos.hegemony_cone_dto import HegemonyConeDTO
from repositories.hegemony_alarms_repository import HegemonyAlarmsRepository
from dtos.hegemony_alarms_dto import HegemonyAlarmsDTO
from typing import Optional, List, Tuple
from datetime import datetime


class HegemonyService:
    def __init__(self):
        self.hegemony_cone_repository = HegemonyConeRepository()
        self.hegemony_alarms_repository = HegemonyAlarmsRepository()

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
        cones, total_count = self.hegemony_cone_repository.get_all(
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

    def get_hegemony_alarms(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        originasn_ids: Optional[List[int]] = None,
        af: Optional[int] = None,
        deviation_gte: Optional[float] = None,
        deviation_lte: Optional[float] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[HegemonyAlarmsDTO], int]:
        """
        Get hegemony alarms data with filtering.
        """
        alarms, total_count = self.hegemony_alarms_repository.get_all(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            asn_ids=asn_ids,
            originasn_ids=originasn_ids,
            af=af,
            deviation_gte=deviation_gte,
            deviation_lte=deviation_lte,
            page=page,
            order_by=order_by
        )

        return [HegemonyAlarmsDTO(
            timebin=alarm.timebin,
            originasn=alarm.originasn,
            asn=alarm.asn,
            deviation=alarm.deviation,
            af=alarm.af,
            asn_name=alarm.asn_relation.name if alarm.asn_relation else None,
            originasn_name=alarm.originasn_relation.name if alarm.originasn_relation else None
        ) for alarm in alarms], total_count
