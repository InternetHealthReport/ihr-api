from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy.orm import Session
from services.network_delay_service import NetworkDelayService
from dtos.generic_response_dto import GenericResponseDTO, build_url
from dtos.network_delay_locations_dto import NetworkDelayLocationsDTO
from dtos.network_delay_dto import NetworkDelayDTO
from dtos.network_delay_alarms_dto import NetworkDelayAlarmsDTO
from config.database import get_db
from typing import Optional, List
from datetime import datetime
from utils import page_size
from utils import *

router = APIRouter(prefix="/network_delay", tags=["Network Delay"])


class NetworkDelayController:
    service = NetworkDelayService()

    @staticmethod
    @router.get("/locations", response_model=GenericResponseDTO[NetworkDelayLocationsDTO])
    @router.get("/locations/", response_model=GenericResponseDTO[NetworkDelayLocationsDTO], include_in_schema=False)
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

    @staticmethod
    @router.get("", response_model=GenericResponseDTO[NetworkDelayDTO])
    @router.get("/", response_model=GenericResponseDTO[NetworkDelayDTO], include_in_schema=False)
    async def get_network_delays(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None,
            description="Timestamp of reported value."
        ),
        timebin__gte: Optional[datetime] = Query(
            None,
            description="Timestamp of reported value."
        ),
        timebin__lte: Optional[datetime] = Query(
            None,
            description="Timestamp of reported value."
        ),
        startpoint_name: Optional[str] = Query(
            None,
            description="Starting location name. It can be a single value or a list of values separated by the pipe character (i.e. | ). The meaning of values dependend on the location type: <ul><li>type=AS: ASN</li><li>type=CT: city name, region name, country code</li><li>type=PB: Atlas Probe ID</li><li>type=IP: IP version (4 or 6)</li></ul> "
        ),
        endpoint_name: Optional[str] = Query(
            None,
            description="Ending location name. It can be a single value or a list of values separated by the pipe character (i.e. | ). The meaning of values dependend on the location type: <ul><li>type=AS: ASN</li><li>type=CT: city name, region name, country code</li><li>type=PB: Atlas Probe ID</li><li>type=IP: IP version (4 or 6)</li></ul> "
        ),
        startpoint_type: Optional[str] = Query(
            None,
            description="Type of starting location. Possible values are: <ul><li>AS: Autonomous System</li><li>CT: City</li><li>PB: Atlas Probe</li><li>IP: Whole IP space</li></ul>"
        ),
        endpoint_type: Optional[str] = Query(
            None,
            description="Type of ending location. Possible values are: <ul><li>AS: Autonomous System</li><li>CT: City</li><li>PB: Atlas Probe</li><li>IP: Whole IP space</li></ul>"
        ),
        startpoint_af: Optional[int] = Query(
            None,
            description="Address Family (IP version), values are either 4 or 6."
        ),
        endpoint_af: Optional[int] = Query(
            None,
            description="Address Family (IP version), values are either 4 or 6."
        ),
        startpoint_key: Optional[str] = Query(
            None,
            description="List of starting location key, separated by the pip character (i.e. | ). A location key is a concatenation of a type, af, and name. For example, CT4New York City, New York, US|AS4174 (yes, the last key corresponds to AS174!)."
        ),
        endpoint_key: Optional[str] = Query(
            None,
            description="List of ending location key, separated by the pip character (i.e. | ). A location key is a concatenation of a type, af, and name. For example, CT4New York City, New York, US|AS4174 (yes, the last key corresponds to AS174!)."
        ),
        median__gte: Optional[float] = Query(
            None, description="Estimated median RTT. RTT values are directly extracted from traceroute (a.k.a. realrtts) and estimated via differential RTTs."),
        median__lte: Optional[float] = Query(
            None, description="Estimated median RTT. RTT values are directly extracted from traceroute (a.k.a. realrtts) and estimated via differential RTTs."),
        median: Optional[float] = Query(
            None, description="Estimated median RTT. RTT values are directly extracted from traceroute (a.k.a. realrtts) and estimated via differential RTTs."),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results.")
    ) -> GenericResponseDTO[NetworkDelayDTO]:
        """
        List estimated network delays between two potentially remote locations. A location can be, for example, an AS, city, Atlas probe.
        <ul>
        <li><b>Required parameters:</b> timebin or a range of timebins (using the two parameters timebin__lte and timebin__gte).</li>
        <li><b>Limitations:</b> At most 7 days of data can be fetched per request. For bulk downloads see: <a href="https://archive.ihr.live/" target="_blank">https://archive.ihr.live/</a>.</li>
        </ul>
        """
        timebin__gte, timebin__lte = validate_timebin_params(
            timebin, timebin__gte, timebin__lte)
        delays, total_count = NetworkDelayController.service.get_network_delays(
            db,
            timebin=timebin,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
            startpoint_names=startpoint_name,
            endpoint_names=endpoint_name,
            startpoint_type=startpoint_type,
            endpoint_type=endpoint_type,
            startpoint_af=startpoint_af,
            endpoint_af=endpoint_af,
            median=median,
            median_gte=median__gte,
            median_lte=median__lte,
            startpoint_key=startpoint_key,
            endpoint_key=endpoint_key,
            page=page,
            order_by=ordering
        )

        next_page = page + 1 if (page * page_size) < total_count else None
        prev_page = page - 1 if page > 1 else None

        return GenericResponseDTO(
            count=total_count,
            next=build_url(request, next_page),
            previous=build_url(request, prev_page),
            results=delays
        )

    @staticmethod
    @router.get("/alarms", response_model=GenericResponseDTO[NetworkDelayAlarmsDTO])
    @router.get("/alarms/", response_model=GenericResponseDTO[NetworkDelayAlarmsDTO], include_in_schema=False)
    async def get_network_delay_alarms(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None,
            description="Timestamp of reported alarm."
        ),
        timebin__gte: Optional[datetime] = Query(
            None,
            description="Timestamp of reported alarm."
        ),
        timebin__lte: Optional[datetime] = Query(
            None,
            description="Timestamp of reported alarm."
        ),
        startpoint_name: Optional[str] = Query(
            None,
            description="Starting location name. It can be a single value or a list of values separated by the pipe character (i.e. | ). The meaning of values dependend on the location type: <ul><li>type=AS: ASN</li><li>type=CT: city name, region name, country code</li><li>type=PB: Atlas Probe ID</li><li>type=IP: IP version (4 or 6)</li></ul> "
        ),
        endpoint_name: Optional[str] = Query(
            None,
            description="Ending location name. It can be a single value or a list of values separated by the pipe character (i.e. | ). The meaning of values dependend on the location type: <ul><li>type=AS: ASN</li><li>type=CT: city name, region name, country code</li><li>type=PB: Atlas Probe ID</li><li>type=IP: IP version (4 or 6)</li></ul> "
        ),
        startpoint_type: Optional[str] = Query(
            None,
            description="Type of starting location. Possible values are: <ul><li>AS: Autonomous System</li><li>CT: City</li><li>PB: Atlas Probe</li><li>IP: Whole IP space</li></ul>"
        ),
        endpoint_type: Optional[str] = Query(
            None,
            description="Type of ending location. Possible values are: <ul><li>AS: Autonomous System</li><li>CT: City</li><li>PB: Atlas Probe</li><li>IP: Whole IP space</li></ul>"
        ),
        startpoint_af: Optional[int] = Query(
            None,
            description="Address Family (IP version), values are either 4 or 6."
        ),
        endpoint_af: Optional[int] = Query(
            None,
            description="Address Family (IP version), values are either 4 or 6."
        ),
        startpoint_key: Optional[str] = Query(
            None,
            description="List of starting location key, separated by the pip character (i.e. | ). A location key is a concatenation of a type, af, and name. For example, CT4New York City, New York, US|AS4174."
        ),
        endpoint_key: Optional[str] = Query(
            None,
            description="List of ending location key, separated by the pip character (i.e. | ). A location key is a concatenation of a type, af, and name. For example, CT4New York City, New York, US|AS4174."
        ),
        deviation__gte: Optional[float] = Query(
            None,
            description="Significance of the AS Hegemony change."
        ),
        deviation__lte: Optional[float] = Query(
            None,
            description="Significance of the AS Hegemony change."
        ),
        page: Optional[int] = Query(
            1, ge=1,
            description="A page number within the paginated result set"
        ),
        ordering: Optional[str] = Query(
            None,
            description="Which field to use when ordering the results."
        )
    ) -> GenericResponseDTO[NetworkDelayAlarmsDTO]:
        """
        List significant network delay changes detected by IHR anomaly detector.
        <ul>
        <li><b>Required parameters:</b> timebin or a range of timebins (using the two parameters timebin__lte and timebin__gte).</li>
        <li><b>Limitations:</b> At most 7 days of data can be fetched per request. For bulk downloads see: <a href="https://archive.ihr.live/" target="_blank">https://archive.ihr.live/</a>.</li>
        </ul>
        """
        timebin__gte, timebin__lte = validate_timebin_params(
            timebin, timebin__gte, timebin__lte)

        alarms, total_count = NetworkDelayController.service.get_network_delay_alarms(
            db,
            timebin=timebin,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
            startpoint_names=startpoint_name,
            endpoint_names=endpoint_name,
            startpoint_type=startpoint_type,
            endpoint_type=endpoint_type,
            startpoint_af=startpoint_af,
            endpoint_af=endpoint_af,
            startpoint_key=startpoint_key,
            endpoint_key=endpoint_key,
            deviation_gte=deviation__gte,
            deviation_lte=deviation__lte,
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
