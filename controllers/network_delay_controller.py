from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from services.network_delay_service import NetworkDelayService
from dtos.generic_response_dto import GenericResponseDTO, build_url
from dtos.network_delay_locations_dto import NetworkDelayLocationsDTO
from config.database import get_db
from typing import Optional
from globals import page_size

router = APIRouter(prefix="/network_delay", tags=["Network Delay"])


class NetworkDelayController:
    service = NetworkDelayService()

    @staticmethod
    @router.get("/locations", response_model=GenericResponseDTO[NetworkDelayLocationsDTO])
    async def get_network_delay_locations(
        request: Request,
        db: Session = Depends(get_db),
        name: Optional[str] = Query(
            None, description="Location identifier, can be searched by substring. The meaning of these values dependend on the location type: "
            "<ul><li>type=AS: ASN</li><li>type=CT: city name, region name, country code</li>"
            "<li>type=PB: Atlas Probe ID</li><li>type=IP: IP version (4 or 6)</li></ul>"),
        type: Optional[str] = Query(
            None, description="Type of location. Possible values are: <ul><li>AS: Autonomous System</li>"
            "<li>CT: City</li><li>PB: Atlas Probe</li><li>IP: Whole IP space</li></ul>"),
        af: Optional[int] = Query(
            None, description="Address Family (IP version), values are either 4 or 6."),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results.")
    ) -> GenericResponseDTO[NetworkDelayLocationsDTO]:
        """
        List locations monitored for network delay measurements. A location can be, for example, an AS, city, Atlas probe.
        """
        locations, total_count = NetworkDelayController.service.get_network_delay_locations(
            db,
            name=name,
            type=type,
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
            results=locations
        )
