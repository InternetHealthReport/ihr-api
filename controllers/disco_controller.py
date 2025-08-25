from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from services.disco_service import DiscoService
from dtos.generic_response_dto import GenericResponseDTO, build_url
from dtos.disco_events_dto import DiscoEventsDTO
from config.database import get_db
from typing import Optional
from datetime import datetime
from utils import page_size

router = APIRouter(prefix="/disco", tags=["Disco"])


class DiscoController:
    service = DiscoService()

    @staticmethod
    @router.get("/events/", response_model=GenericResponseDTO[DiscoEventsDTO])
    async def get_events(
        request: Request,
        db: Session = Depends(get_db),
        streamname: Optional[str] = Query(
            None, description="Name of the topological (ASN) or geographical area where the network disconnection happened."),
        streamtype: Optional[str] = Query(
            None, description="Granularity of the detected event. The possible values are asn, country, admin1, and admin2. Admin1 represents a wider area than admin2, the exact definition might change from one country to another. For example 'California, US' is an admin1 stream and 'San Francisco County, California, US' is an admin2 stream."),
        starttime: Optional[datetime] = Query(
            None, description="Estimated start time of the network disconnection."),
        starttime__gte: Optional[datetime] = Query(
            None, description="Estimated start time of the network disconnection."),
        starttime__lte: Optional[datetime] = Query(
            None, description="Estimated start time of the network disconnection."),
        endtime: Optional[datetime] = Query(
            None, description="Estimated end time of the network disconnection. Equal to starttime if the end of the event is unknown."),
        endtime__gte: Optional[datetime] = Query(
            None, description="Estimated end time of the network disconnection. Equal to starttime if the end of the event is unknown."),
        endtime__lte: Optional[datetime] = Query(
            None, description="Estimated end time of the network disconnection. Equal to starttime if the end of the event is unknown."),
        avglevel: Optional[float] = Query(
            None, description="Score representing the coordination of disconnected probes. Higher values stand for a large number of Atlas probes that disconnected in a very short time frame. Events with an avglevel lower than 10 are likely to be false positives detection."),
        avglevel__gte: Optional[float] = Query(
            None, description="Score representing the coordination of disconnected probes. Higher values stand for a large number of Atlas probes that disconnected in a very short time frame. Events with an avglevel lower than 10 are likely to be false positives detection."),
        avglevel__lte: Optional[float] = Query(
            None, description="Score representing the coordination of disconnected probes. Higher values stand for a large number of Atlas probes that disconnected in a very short time frame. Events with an avglevel lower than 10 are likely to be false positives detection."),
        nbdiscoprobes: Optional[int] = Query(
            None, description="NNumber of Atlas probes that disconnected around the reported start time."),
        nbdiscoprobes__gte: Optional[int] = Query(
            None, description="Number of Atlas probes that disconnected around the reported start time."),
        nbdiscoprobes__lte: Optional[int] = Query(
            None, description="Number of Atlas probes that disconnected around the reported start time."),
        totalprobes: Optional[int] = Query(
            None, description="Total number of Atlas probes active in the reported stream (ASN, Country, or geographical area)."),
        totalprobes__gte: Optional[int] = Query(
            None, description="Total number of Atlas probes active in the reported stream (ASN, Country, or geographical area)."),
        totalprobes__lte: Optional[int] = Query(
            None, description="Total number of Atlas probes active in the reported stream (ASN, Country, or geographical area)."),
        ongoing: Optional[str] = Query(
            None, description="Deprecated, this value is unused"),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set."),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results")
    ) -> GenericResponseDTO[DiscoEventsDTO]:
        """
        List network disconnections detected with RIPE Atlas. 
        These events have different levels of granularity - it can be at a network level (AS), city, or country level.
        """

        events_data, total_count = DiscoController.service.get_disco_events(
            db,
            streamname=streamname,
            streamtype=streamtype,
            starttime=starttime,
            starttime_gte=starttime__gte,
            starttime_lte=starttime__lte,
            endtime=endtime,
            endtime_gte=endtime__gte,
            endtime_lte=endtime__lte,
            avglevel=avglevel,
            avglevel_gte=avglevel__gte,
            avglevel_lte=avglevel__lte,
            nbdiscoprobes=nbdiscoprobes,
            nbdiscoprobes_gte=nbdiscoprobes__gte,
            nbdiscoprobes_lte=nbdiscoprobes__lte,
            totalprobes=totalprobes,
            totalprobes_gte=totalprobes__gte,
            totalprobes_lte=totalprobes__lte,
            ongoing=ongoing,
            page=page,
            order_by=ordering
        )

        next_page = page + 1 if (page * page_size) < total_count else None
        prev_page = page - 1 if page > 1 else None

        return GenericResponseDTO(
            count=total_count,
            next=build_url(request, next_page),
            previous=build_url(request, prev_page),
            results=events_data
        )
