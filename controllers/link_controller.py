from fastapi import APIRouter, Depends, Query, Request, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from services.link_service import LinkService
from dtos.generic_response_dto import GenericResponseDTO, build_url
from dtos.link_delay_dto import LinkDelayDTO
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
        timebin_gte: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        timebin_lte: Optional[datetime] = Query(
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
        timebin_gte, timebin_lte = validate_timebin_params(timebin, timebin_gte, timebin_lte)

        # Convert comma-separated ASNs to list
        asn_list = [int(x.strip()) for x in asn.split(",")] if asn else None

        delays, total_count = LinkController.service.get_link_delays(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
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
