from fastapi import APIRouter, Depends, Query, Request, Response, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from services.hegemony_cone_service import HegemonyConeService
from dtos.generic_response_dto import GenericResponseDTO, build_url
from dtos.hegemony_cone_dto import HegemonyConeDTO
from config.database import get_db
from typing import Optional, List
from globals import page_size

router = APIRouter(prefix="/hegemony/cones", tags=["Hegemony Cones"])


class HegemonyConeController:
    service = HegemonyConeService()

    @staticmethod
    @router.get("/", response_model=GenericResponseDTO[HegemonyConeDTO])
    async def get_hegemony_cones(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None, description="Get results for exact timestamp"),
        timebin_gte: Optional[datetime] = Query(
            None, description="Get results after or equal to this timestamp"),
        timebin_lte: Optional[datetime] = Query(
            None, description="Get results before or equal to this timestamp"),
        asn: Optional[str] = Query(
            None, description="Autonomous System Number (ASN). Can be a single value or a list of comma separated values."),
        af: Optional[int] = Query(
            None, description="Address Family (IP version) either 4 or 6"),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results")
    ) -> GenericResponseDTO[HegemonyConeDTO]:
        """
         The number of networks that depend on a given network. This is similar to CAIDA's customer cone size.
         <ul>
         <li><b>Required parameters:</b> timebin or a range of timebins (using the two parameters timebin__lte and timebin__gte).</li>
         <li><b>Limitations:</b> At most 7 days of data can be fetched per request. For bulk downloads see: <a href="https://ihr-archive.iijlab.net/" target="_blank">https://ihr-archive.iijlab.net/</a>.</li>
         </ul>
         networks).
        """
        # Check if at least one time parameter exists
        if not any([timebin, timebin_gte, timebin_lte]):
            raise HTTPException(
                status_code=400,
                detail="No timebin parameter. Please provide a timebin value or a range of values with timebin__lte and timebin__gte."
            )

        # If timebin is not provided, both timebin_gte and timebin_lte must be provided
        if not timebin and not (timebin_gte and timebin_lte):
            raise HTTPException(
                status_code=400,
                detail="Invalid timebin range. Please provide both timebin__lte and timebin__gte."
            )

        # If exact timebin is provided, it overrides the range parameters
        if timebin:
            timebin_gte = timebin
            timebin_lte = timebin

        # Validate date range (max 7 days)
        if timebin_gte and timebin_lte:
            delta = timebin_lte - timebin_gte
            if delta > timedelta(days=7):
                raise HTTPException(
                    status_code=400,
                    detail="The given timebin range is too large. Should be less than 7 days."
                )

        # Convert comma-separated ASNs to list
        asn_list = [int(x.strip()) for x in asn.split(",")] if asn else None

        cones, total_count = HegemonyConeController.service.get_hegemony_cones(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            asn_ids=asn_list,
            af=af,
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
            results=cones
        )
