from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from services.networks_service import NetworksService
from dtos.networks_dto import NetworksDTO
from dtos.generic_response_dto import GenericResponseDTO, build_url
from config.database import get_db
from utils import page_size

router = APIRouter(prefix="/networks", tags=["Networks"])


class NetworksController:
    service = NetworksService()

    @staticmethod
    @router.get("", response_model=GenericResponseDTO[NetworksDTO])
    @router.get("/", response_model=GenericResponseDTO[NetworksDTO], include_in_schema=False)
    async def get_networks(
        request: Request,
        db: Session = Depends(get_db),
        name: Optional[str] = Query(
            None, description="Search for a substring in networks name"),
        number: Optional[str] = Query(
            None, description="Search by ASN or IXP ID. It can be either a single value (e.g. 2497) or a list of comma separated values (e.g. 2497,2500,2501)"),
        number__gte: Optional[int] = Query(
            None, description="Autonomous System Number (ASN) or IXP ID. Note that IXP ID are negative to avoid colision."),
        number__lte: Optional[int] = Query(
            None, description="Autonomous System Number (ASN) or IXP ID. Note that IXP ID are negative to avoid colision."),
        search: Optional[str] = Query(
            None, description="Search for both ASN/IXPID and substring in names"),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set."),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results.")
    ) -> GenericResponseDTO[NetworksDTO]:
        """
        List networks referenced on IHR (see. /network_delay/locations/ for network delay locations). 
        Can be searched by keyword, ASN, or IXPID. Range of ASN/IXPID can be obtained with parameters number__lte and number__gte.
        """
        # Convert comma-separated numbers to list if provided
        number_list = [int(x.strip())
                       for x in number.split(",")] if number else None

        networks, total_count = NetworksController.service.get_networks(
            db,
            name=name,
            numbers=number_list,
            number_gte=number__gte,
            number_lte=number__lte,
            search=search,
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
            results=networks
        )
