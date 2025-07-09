from fastapi import APIRouter, Depends, Query, Request
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from services.metis_service import MetisService
from dtos.generic_response_dto import GenericResponseDTO, build_url
from dtos.metis_atlas_deployment_dto import MetisAtlasDeploymentDTO
from config.database import get_db
from typing import Optional
from globals import page_size
from utils import validate_timebin_params, prepare_timebin_range

router = APIRouter(prefix="/metis/atlas", tags=["Metis"])


class MetisController:
    service = MetisService()

    @staticmethod
    @router.get("/deployment", response_model=GenericResponseDTO[MetisAtlasDeploymentDTO])
    async def get_metis_atlas_deployments(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None, description="Time when the ranking is computed. The ranking uses 24 weeks of data, hence 2022-05-23T00:00 means the ranking using data from 2021-12-06T00:00 to 2022-05-23T00:00."),
        timebin__gte: Optional[datetime] = Query(
            None, description="Time when the ranking is computed. The ranking uses 24 weeks of data, hence 2022-05-23T00:00 means the ranking using data from 2021-12-06T00:00 to 2022-05-23T00:00."),
        timebin__lte: Optional[datetime] = Query(
            None, description="Time when the ranking is computed. The ranking uses 24 weeks of data, hence 2022-05-23T00:00 means the ranking using data from 2021-12-06T00:00 to 2022-05-23T00:00."),
        rank: Optional[int] = Query(
            None, description="Selecting all ASes with rank less than equal to 10 (i.e. rank__lte=10), gives the 10 most diverse ASes in terms of the selected metric."),
        rank__lte: Optional[int] = Query(
            None, description="Selecting all ASes with rank less than equal to 10 (i.e. rank__lte=10), gives the 10 most diverse ASes in terms of the selected metric."),
        rank__gte: Optional[int] = Query(
            None, description="Selecting all ASes with rank less than equal to 10 (i.e. rank__lte=10), gives the 10 most diverse ASes in terms of the selected metric."),
        metric: Optional[str] = Query(
            None, description="Distance metric used to compute diversity, possible values are: 'as_path_length', 'ip_hops', 'rtt'"),
        af: Optional[int] = Query(
            None, description="Address Family (IP version), values are either 4 or 6"),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results.")
    ) -> GenericResponseDTO[MetisAtlasDeploymentDTO]:
        """
        Metis identifies ASes that are far from Atlas probes. Deploying Atlas probes in these ASes would be beneficial for Atlas coverage.
        <ul>
        <li><b>Limitations:</b> At most 31 days of data can be fetched per request. For bulk downloads see: <a href="https://ihr-archive.iijlab.net/" target="_blank">https://ihr-archive.iijlab.net/</a>.</li>
        </ul>
        """
        timebin__gte, timebin__lte = prepare_timebin_range(
            timebin, timebin__gte, timebin__lte, max_days=31)

        deployments, total_count = MetisController.service.get_metis_atlas_deployments(
            db,
            timebin=timebin,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
            rank=rank,
            rank_lte=rank__lte,
            rank_gte=rank__gte,
            metric=metric,
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
            results=deployments
        )
