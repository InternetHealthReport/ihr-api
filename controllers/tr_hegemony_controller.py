from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from services.tr_hegemony_service import TRHegemonyService
from dtos.generic_response_dto import GenericResponseDTO, build_url
from dtos.tr_hegemony_dto import TRHegemonyDTO
from config.database import get_db
from typing import Optional
from datetime import datetime
from utils import page_size
from utils import prepare_timebin_range

router = APIRouter(prefix="/tr_hegemony", tags=["TR Hegemony"])


class TRHegemonyController:
    service = TRHegemonyService()

    @staticmethod
    @router.get("/", response_model=GenericResponseDTO[TRHegemonyDTO])
    async def get_hegemony(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None, description="Timestamp of reported value. The computation uses four weeks of data, hence 2022-03-28T00:00 means the values are based on data from 2022-02-28T00:00 to 2022-03-28T00:00."),
        timebin__gte: Optional[datetime] = Query(
            None, description="Timestamp of reported value. The computation uses four weeks of data, hence 2022-03-28T00:00 means the values are based on data from 2022-02-28T00:00 to 2022-03-28T00:00."),
        timebin__lte: Optional[datetime] = Query(
            None, description="Timestamp of reported value. The computation uses four weeks of data, hence 2022-03-28T00:00 means the values are based on data from 2022-02-28T00:00 to 2022-03-28T00:00."),
        origin_name: Optional[str] = Query(
            None, description="Origin name. It can be a single value or a list of values separated by the pipe character (i.e. | ). The meaning of values depends on the identifier type: <ul><li>type=AS: ASN</li><li>type=IX: PeeringDB IX ID</li><li>type=MB: IXP member (format: ix_id;asn)</li><li>type=IP: Interface IP of an IXP member</li></ul>"),
        dependency_name: Optional[str] = Query(
            None, description="Dependency name. It can be a single value or a list of values separated by the pipe character (i.e. | ). The meaning of values depends on the identifier type: <ul><li>type=AS: ASN</li><li>type=IX: PeeringDB IX ID</li><li>type=MB: IXP member (format: ix_id;asn)</li><li>type=IP: Interface IP of an IXP member</li></ul>"),
        origin_type: Optional[str] = Query(
            None, description="Type of the origin. Possible values are: <ul><li>AS: Autonomous System</li><li>IX: IXP</li><li>MB: IXP member</li><li>IP: IXP member IP</li></ul>"),
        dependency_type: Optional[str] = Query(
            None, description="Type of the dependency. Possible values are: <ul><li>AS: Autonomous System</li><li>IX: IXP</li><li>MB: IXP member</li><li>IP: IXP member IP</li></ul>"),
        origin_af: Optional[int] = Query(
            None, description="Address family (IP version) of the origin. Values are either 4 or 6."),
        dependency_af: Optional[int] = Query(
            None, description="Address family (IP version) of the dependency. Values are either 4 or 6."),
        hege: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the origin. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        hege__gte: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the origin. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        hege__lte: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the origin. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        af: Optional[int] = Query(
            None, description="Address family (IP version), values are either 4 or 6."),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results.")
    ) -> GenericResponseDTO[TRHegemonyDTO]:
        """
        List AS and IXP dependencies for all ASes visible in monitored traceroute data.
        <ul>
        <li><b>Limitations:</b> At most 31 days of data can be fetched per request. For bulk downloads see: <a href="https://ihr-archive.iijlab.net/" target="_blank">https://ihr-archive.iijlab.net/</a>.</li>
        </ul>
        """
        timebin__gte, timebin__lte = prepare_timebin_range(
            timebin, timebin__gte, timebin__lte, max_days=31)

        hegemony_data, total_count = TRHegemonyController.service.get_tr_hegemony(
            db,
            timebin=timebin,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
            origin_names=origin_name,
            dependency_names=dependency_name,
            origin_type=origin_type,
            dependency_type=dependency_type,
            origin_af=origin_af,
            dependency_af=dependency_af,
            hege=hege,
            hege_gte=hege__gte,
            hege_lte=hege__lte,
            af=af,
            page=page,
            order_by=ordering
        )

        next_page = page + 1 if (page * page_size) < total_count else None
        prev_page = page - 1 if page > 1 else None

        return GenericResponseDTO(
            count=total_count,
            next=build_url(request, next_page),
            previous=build_url(request, prev_page),
            results=hegemony_data
        )
