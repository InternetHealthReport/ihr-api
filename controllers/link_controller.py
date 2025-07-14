from fastapi import APIRouter, Depends, Query, Request, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from services.link_service import LinkService
from dtos.generic_response_dto import GenericResponseDTO, build_url
from dtos.link_delay_dto import LinkDelayDTO
from dtos.link_forwarding_dto import LinkForwardingDTO
from dtos.link_delay_alarms_dto import LinkDelayAlarmsDTO
from config.database import get_db
from typing import Optional
from globals import page_size
from utils import validate_timebin_params

router = APIRouter(prefix="/link", tags=["Link"])


class LinkController:
    service = LinkService()

    @staticmethod
    @router.get("/delay", response_model=GenericResponseDTO[LinkDelayDTO])
    async def get_link_delays(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        timebin__gte: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        timebin__lte: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        asn: Optional[str] = Query(
            None, description="ASN or IXP ID of the monitored network (see number in /network/). Can be a single value or a list of comma separated values."),
        magnitude: Optional[float] = Query(
            None, description="Cumulated link delay deviation. Values close to zero represent usual delays for the network, whereas higher values stand for significant links congestion in the monitored network."),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results.")
    ) -> GenericResponseDTO[LinkDelayDTO]:
        """
        List cumulated link delay changes (magnitude) for each monitored network.  Magnitude values close to zero represent usual delays for the network, whereas higher values stand for significant links congestion in the monitored network.
        The details of each congested link is available in /delay/alarms/.
        <ul>
        <li><b>Required parameters:</b> timebin or a range of timebins (using the two parameters timebin__lte and timebin__gte).</li>
        <li><b>Limitations:</b> At most 7 days of data can be fetched per request. For bulk downloads see: <a href="https://ihr-archive.iijlab.net/" target="_blank">https://ihr-archive.iijlab.net/</a>.</li>
        </ul>
        """
        timebin__gte, timebin__lte = validate_timebin_params(
            timebin, timebin__gte, timebin__lte)

        # Convert comma-separated ASNs to list
        asn_list = [int(x.strip()) for x in asn.split(",")] if asn else None

        delays, total_count = LinkController.service.get_link_delays(
            db,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
            asn_ids=asn_list,
            magnitude=magnitude,
            page=page,
            order_by=ordering
        )

        # Calculate pagination
        next_page = page + 1 if (page * page_size) < total_count else None
        prev_page = page - 1 if page > 1 else None

        return GenericResponseDTO(
            count=total_count,
            next=build_url(request, next_page),
            previous=build_url(request, prev_page),
            results=delays
        )

    @staticmethod
    @router.get("/forwarding", response_model=GenericResponseDTO[LinkForwardingDTO])
    async def get_link_forwardings(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        timebin__gte: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        timebin__lte: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        asn: Optional[str] = Query(
            None, description="ASN or IXP ID of the monitored network (see number in /network/). Can be a single value or a list of comma separated values."),
        magnitude: Optional[float] = Query(
            None, description="Cumulated forwarding anomaly deviation for each monitored network. Values close to zero represent usual forwarding paths for the network, whereas higher positive (resp. negative) values stand for an increasing (resp. decreasing) number of paths passing through the monitored network."),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results.")
    ) -> GenericResponseDTO[LinkForwardingDTO]:
        """
        List cumulated forwarding anomaly deviation (magnitude) for each monitored network. 
        Magnitude values close to zero represent usual forwarding paths for the network, whereas 
        higher positive (resp. negative) values stand for an increasing (resp. decreasing) 
        number of paths passing through the monitored network.
        The details of each forwarding anomaly is available in /forwarding/alarms/.
        <ul>
        <li><b>Required parameters:</b> timebin or a range of timebins (using the two parameters timebin__lte and timebin__gte).</li>
        <li><b>Limitations:</b> At most 7 days of data can be fetched per request. For bulk downloads see: <a href="https://ihr-archive.iijlab.net/" target="_blank">https://ihr-archive.iijlab.net/</a>.</li>
        </ul>
        """
        timebin__gte, timebin__lte = validate_timebin_params(
            timebin, timebin__gte, timebin__lte)

        # Convert comma-separated ASNs to list
        asn_list = [int(x.strip()) for x in asn.split(",")] if asn else None

        forwardings, total_count = LinkController.service.get_link_forwardings(
            db,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
            asn_ids=asn_list,
            magnitude=magnitude,
            page=page,
            order_by=ordering
        )

        # Calculate pagination
        next_page = page + 1 if (page * page_size) < total_count else None
        prev_page = page - 1 if page > 1 else None

        return GenericResponseDTO(
            count=total_count,
            next=build_url(request, next_page),
            previous=build_url(request, prev_page),
            results=forwardings
        )

    @staticmethod
    @router.get("/delay/alarms", response_model=GenericResponseDTO[LinkDelayAlarmsDTO])
    async def get_link_delay_alarms(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None, description="Timestamp of reported alarm."),
        timebin__gte: Optional[datetime] = Query(
            None, description="Timestamp of reported alarm."),
        timebin__lte: Optional[datetime] = Query(
            None, description="Timestamp of reported alarm."),
        asn: Optional[str] = Query(
            None, description="ASN or IXP ID of the monitored network (see number in /network/). Can be a single value or a list of comma separated values."),
        deviation: Optional[float] = Query(
            None, description="Distance between observed delays and the past usual values normalized by median absolute deviation."),
        deviation__gte: Optional[float] = Query(
            None, description="Distance between observed delays and the past usual values normalized by median absolute deviation."),
        deviation__lte: Optional[float] = Query(
            None, description="Distance between observed delays and the past usual values normalized by median absolute deviation."),
        diffmedian: Optional[float] = Query(
            None, description="Difference between the link usual median RTT and the median RTT observed during the alarm."),
        diffmedian__gte: Optional[float] = Query(
            None, description="Difference between the link usual median RTT and the median RTT observed during the alarm."),
        diffmedian__lte: Optional[float] = Query(
            None, description="Difference between the link usual median RTT and the median RTT observed during the alarm."),
        medianrtt: Optional[float] = Query(
            None, description="Median differential RTT observed during the alarm."),
        medianrtt__gte: Optional[float] = Query(
            None, description="Median differential RTT observed during the alarm."),
        medianrtt__lte: Optional[float] = Query(
            None, description="Median differential RTT observed during the alarm."),
        nbprobes: Optional[int] = Query(
            None, description="Number of Atlas probes monitoring this link at the reported time window."),
        nbprobes__gte: Optional[int] = Query(
            None, description="Number of Atlas probes monitoring this link at the reported time window."),
        nbprobes__lte: Optional[int] = Query(
            None, description="Number of Atlas probes monitoring this link at the reported time window."),
        link: Optional[str] = Query(None, description="Pair of IP addresses corresponding to the reported link."),
        link__contains: Optional[str] = Query(
            None, description="Pair of IP addresses corresponding to the reported link."),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results.")
    ) -> GenericResponseDTO[LinkDelayAlarmsDTO]:
        """
        List detected link delay changes.
        <ul>
        <li><b>Required parameters:</b> timebin or a range of timebins (using the two parameters timebin__lte and timebin__gte).</li>
        <li><b>Limitations:</b> At most 7 days of data can be fetched per request. For bulk downloads see: <a href="https://ihr-archive.iijlab.net/" target="_blank">https://ihr-archive.iijlab.net/</a>.</li>
        </ul>
        """
        timebin__gte, timebin__lte = validate_timebin_params(
            timebin, timebin__gte, timebin__lte)

        # Convert comma-separated ASNs to list
        asn_list = [int(x.strip()) for x in asn.split(",")] if asn else None

        alarms, total_count = LinkController.service.get_link_delay_alarms(
            db,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
            asn_ids=asn_list,
            deviation_gte=deviation__gte,
            deviation_lte=deviation__lte,
            diffmedian_gte=diffmedian__gte,
            diffmedian_lte=diffmedian__lte,
            medianrtt_gte=medianrtt__gte,
            medianrtt_lte=medianrtt__lte,
            nbprobes_gte=nbprobes__gte,
            nbprobes_lte=nbprobes__lte,
            link=link,
            link_contains=link__contains,
            page=page,
            order_by=ordering
        )

        next_page = page + 1 if (page * page_size) < total_count else None
        prev_page = page - 1 if page > 1 else None

        return GenericResponseDTO(
            count=total_count,
            next=build_url(request, next_page),
            previous=build_url(request, prev_page),
            results=alarms
        )
