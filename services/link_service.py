from sqlalchemy.orm import Session
from repositories.delay_repository import DelayRepository
from dtos.link_delay_dto import LinkDelayDTO
from repositories.forwarding_repository import ForwardingRepository
from dtos.link_forwarding_dto import LinkForwardingDTO
from typing import Optional, List, Tuple
from datetime import datetime
from repositories.delay_alarms_repository import DelayAlarmsRepository
from dtos.link_delay_alarms_dto import LinkDelayAlarmsDTO


class LinkService:
    def __init__(self):
        self.delay_repository = DelayRepository()
        self.forwarding_repository = ForwardingRepository()
        self.delay_alarms_repository = DelayAlarmsRepository()

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

    def get_link_forwardings(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        magnitude: Optional[float] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[LinkForwardingDTO], int]:
        """
        Get link forwarding data with filtering.
        """
        forwardings, total_count = self.forwarding_repository.get_all(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            asn_ids=asn_ids,
            magnitude=magnitude,
            page=page,
            order_by=order_by
        )

        return [LinkForwardingDTO(
            timebin=forwarding.timebin,
            asn=forwarding.asn,
            magnitude=forwarding.magnitude,
            asn_name=forwarding.asn_relation.name if forwarding.asn_relation else None
        ) for forwarding in forwardings], total_count

    def get_link_delay_alarms(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        deviation_gte: Optional[float] = None,
        deviation_lte: Optional[float] = None,
        diffmedian_gte: Optional[float] = None,
        diffmedian_lte: Optional[float] = None,
        medianrtt_gte: Optional[float] = None,
        medianrtt_lte: Optional[float] = None,
        nbprobes_gte: Optional[int] = None,
        nbprobes_lte: Optional[int] = None,
        link: Optional[str] = None,
        link_contains: Optional[str] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[LinkDelayAlarmsDTO], int]:
        """
        Get link delay alarms data with filtering.
        """
        alarms, total_count = self.delay_alarms_repository.get_all(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            asn_ids=asn_ids,
            deviation_gte=deviation_gte,
            deviation_lte=deviation_lte,
            diffmedian_gte=diffmedian_gte,
            diffmedian_lte=diffmedian_lte,
            medianrtt_gte=medianrtt_gte,
            medianrtt_lte=medianrtt_lte,
            nbprobes_gte=nbprobes_gte,
            nbprobes_lte=nbprobes_lte,
            link=link,
            link_contains=link_contains,
            page=page,
            order_by=order_by
        )

        return [LinkDelayAlarmsDTO(
            timebin=alarm.timebin,
            asn=alarm.asn,
            asn_name=alarm.asn_relation.name if alarm.asn_relation else None,
            link=alarm.link,
            medianrtt=alarm.medianrtt,
            diffmedian=alarm.diffmedian,
            deviation=alarm.deviation,
            nbprobes=alarm.nbprobes,
            msm_prb_ids=alarm.msm_prb_ids
        ) for alarm in alarms], total_count
