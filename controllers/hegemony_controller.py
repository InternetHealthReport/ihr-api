from dtos.hegemony_country_dto import HegemonyCountryDTO
from dtos.hegemony_dto import HegemonyDTO
from dtos.hegemony_prefix_dto import HegemonyPrefixDTO
from fastapi import APIRouter, Depends, Query, Request, Response, HTTPException, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from services.hegemony_service import HegemonyService
from dtos.generic_response_dto import GenericResponseDTO, build_url
from dtos.hegemony_cone_dto import HegemonyConeDTO
from dtos.hegemony_alarms_dto import HegemonyAlarmsDTO
from config.database import get_db
from typing import Optional, List
from utils import page_size
from utils import *

router = APIRouter(prefix="/hegemony", tags=["Hegemony"])


class HegemonyController:
    service = HegemonyService()

    @staticmethod
    @router.get("", response_model=GenericResponseDTO[HegemonyDTO])
    @router.get("/", response_model=GenericResponseDTO[HegemonyDTO])
    async def get_hegemony(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        timebin__gte: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        timebin__lte: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        asn: Optional[str] = Query(
            None, description="Dependency. Transit network commonly seen in BGP paths towards originasn. Can be a single value or a list of comma separated values."),
        originasn: Optional[str] = Query(
            None, description="Dependent network, it can be any public ASN. Can be a single value or a list of comma separated values. Retrieve all dependencies of a network by setting a single value and a timebin."),
        af: Optional[int] = Query(
            None, description="Address Family (IP version), values are either 4 or 6."),
        hege: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the originasn. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        hege__gte: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the originasn. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        hege__lte: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the originasn. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results")
    ) -> GenericResponseDTO[HegemonyDTO]:
        """
        List AS dependencies for all ASes visible in monitored BGP data. This endpoint also provides the AS dependency to the entire IP space (a.k.a. global graph) which is available by setting the originasn parameter to 0.
        <ul>
        <li><b>Required parameters:</b> timebin or a range of timebins (using the two parameters timebin__lte and timebin__gte).</li>
        <li><b>Limitations:</b> At most 7 days of data can be fetched per request. For bulk downloads see: <a href="https://archive.ihr.live/" target="_blank">https://archive.ihr.live/</a>.</li>
        </ul>
        """
        timebin__gte, timebin__lte = validate_timebin_params(
            timebin, timebin__gte, timebin__lte)

        # Convert comma-separated ASNs to lists
        asn_list = [int(x.strip()) for x in asn.split(",")] if asn else None
        originasn_list = [int(x.strip())
                          for x in originasn.split(",")] if originasn else None

        # Ensure either asn or originasn is provided
        if not asn and not originasn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Required parameter missing. Please provide one of the following parameters: ['originasn', 'asn']"
            )

        hegemony_data, total_count = HegemonyController.service.get_hegemony(
            db,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
            asn_ids=asn_list,
            originasn_ids=originasn_list,
            af=af,
            hege=hege,
            hege_gte=hege__gte,
            hege_lte=hege__lte,
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
            results=hegemony_data
        )

    @staticmethod
    @router.get("/cones", response_model=GenericResponseDTO[HegemonyConeDTO])
    @router.get("/cones/", response_model=GenericResponseDTO[HegemonyConeDTO])
    async def get_hegemony_cones(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None, description="Get results for exact timestamp"),
        timebin__gte: Optional[datetime] = Query(
            None, description="Get results after or equal to this timestamp"),
        timebin__lte: Optional[datetime] = Query(
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
         <li><b>Limitations:</b> At most 7 days of data can be fetched per request. For bulk downloads see: <a href="https://archive.ihr.live/" target="_blank">https://archive.ihr.live/</a>.</li>
         </ul>
         networks).
        """
        timebin__gte, timebin__lte = validate_timebin_params(
            timebin, timebin__gte, timebin__lte)

        # Convert comma-separated ASNs to list
        asn_list = [int(x.strip()) for x in asn.split(",")] if asn else None

        cones, total_count = HegemonyController.service.get_hegemony_cones(
            db,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
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

    @staticmethod
    @router.get("/alarms", response_model=GenericResponseDTO[HegemonyAlarmsDTO])
    @router.get("/alarms/", response_model=GenericResponseDTO[HegemonyAlarmsDTO])
    async def get_hegemony_alarms(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None, description="Timestamp of reported alarm."),
        timebin__gte: Optional[datetime] = Query(
            None, description="Timestamp of reported alarm."),
        timebin__lte: Optional[datetime] = Query(
            None, description="Timestamp of reported alarm."),
        asn: Optional[str] = Query(
            None, description="ASN of the anomalous dependency (transit network). Can be a single value or a list of comma separated values."),
        originasn: Optional[str] = Query(
            None, description="ASN of the reported dependent network. Can be a single value or a list of comma separated values."),
        af: Optional[int] = Query(
            None, description="Address Family (IP version), values are either 4 or 6."),
        deviation__gte: Optional[float] = Query(
            None, description="Significance of the AS Hegemony change."),
        deviation__lte: Optional[float] = Query(
            None, description="Significance of the AS Hegemony change."),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results")
    ) -> GenericResponseDTO[HegemonyAlarmsDTO]:
        """
        List significant AS dependency changes detected by IHR anomaly detector.
        <ul>
        <li><b>Required parameters:</b> timebin or a range of timebins (using the two parameters timebin__lte and timebin__gte).</li>
        <li><b>Limitations:</b> At most 7 days of data can be fetched per request. For bulk downloads see: <a href="https://archive.ihr.live/" target="_blank">https://archive.ihr.live/</a>.</li>
        </ul>
        """
        timebin__gte, timebin__lte = validate_timebin_params(
            timebin, timebin__gte, timebin__lte)

        # Convert comma-separated ASNs to lists
        asn_list = [int(x.strip()) for x in asn.split(",")] if asn else None
        originasn_list = [int(x.strip())
                          for x in originasn.split(",")] if originasn else None

        alarms, total_count = HegemonyController.service.get_hegemony_alarms(
            db,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
            asn_ids=asn_list,
            originasn_ids=originasn_list,
            af=af,
            deviation_gte=deviation__gte,
            deviation_lte=deviation__lte,
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
            results=alarms
        )

    @staticmethod
    @router.get("/countries", response_model=GenericResponseDTO[HegemonyCountryDTO])
    @router.get("/countries/", response_model=GenericResponseDTO[HegemonyCountryDTO])
    async def get_hegemony_countries(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        timebin__gte: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        timebin__lte: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        asn: Optional[str] = Query(
            None, description="Dependency. Network commonly seen in BGP paths towards monitored country. Can be a single value or a list of comma separated values."),
        country: Optional[str] = Query(
            None, description="Monitored country or region (e.g. EU and AP) as defined by its set of ASes registered in registeries delegated files. Can be a single value or a list of comma separated values. Retrieve all dependencies of a country by setting a single value and a timebin."),
        af: Optional[int] = Query(
            None, description="Address Family (IP version), values are either 4 or 6."),
        weightscheme: Optional[str] = Query(
            None, description="Scheme used to aggregate AS Hegemony scores. 'as' gives equal weight to each AS, 'eyeball' put emphasis on large eyeball networks."),
        transitonly: Optional[bool] = Query(
            None, description="True means that the last AS (origin AS) in BGP paths is ignored, thus focusing only on transit ASes."),
        hege: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the monitored country. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        hege__gte: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the monitored country. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        hege__lte: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the monitored country. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results")
    ) -> GenericResponseDTO[HegemonyCountryDTO]:
        """
        List AS dependencies of countries. A country infrastructure is defined by its ASes registed in RIRs delegated files. Emphasis can be put on eyeball users with the eyeball weighting scheme (i.e. weightscheme='eyeball').
        <ul>
        <li><b>Required parameters:</b> timebin or a range of timebins (using the two parameters timebin__lte and timebin__gte).</li>
        <li><b>Limitations:</b> At most 31 days of data can be fetched per request. For bulk downloads see: <a href="https://archive.ihr.live/" target="_blank">https://archive.ihr.live/</a>.</li>
        </ul>
        """
        timebin__gte, timebin__lte = validate_timebin_params(
            timebin, timebin__gte, timebin__lte, max_days=31)

        # Ensure either `asn` or `country` is provided
        if not asn and not country:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Required parameter missing. Please provide one of the following parameters: ['country', 'asn']"
            )

        # Convert comma-separated values to lists
        asn_list = [int(x.strip()) for x in asn.split(",")] if asn else None
        country_list = [x.strip()
                        for x in country.split(",")] if country else None

        countries, total_count = HegemonyController.service.get_hegemony_countries(
            db,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
            asn_ids=asn_list,
            countries=country_list,
            af=af,
            weightscheme=weightscheme,
            transitonly=transitonly,
            hege=hege,
            hege_gte=hege__gte,
            hege_lte=hege__lte,
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
            results=countries
        )

    @staticmethod
    @router.get("/prefixes", response_model=GenericResponseDTO[HegemonyPrefixDTO])
    @router.get("/prefixes/", response_model=GenericResponseDTO[HegemonyPrefixDTO])
    async def get_hegemony_prefixes(
        request: Request,
        db: Session = Depends(get_db),
        timebin: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        timebin__gte: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        timebin__lte: Optional[datetime] = Query(
            None, description="Timestamp of reported value."),
        prefix: Optional[str] = Query(
            None, description="Monitored prefix, it can be any globally reachable prefix. Can be a single value or a list of comma separated values."),
        asn: Optional[str] = Query(
            None, description="Dependency. Network commonly seen in BGP paths towards monitored prefix. Can be a single value or a list of comma separated values."),
        originasn: Optional[str] = Query(
            None, description="Origin network, it can be any public ASN. Can be a single value or a list of comma separated values."),
        country: Optional[str] = Query(
            None, description="Country code for prefixes as reported by Maxmind's Geolite2 geolocation database. Can be a single value or a list of comma separated values. Retrieve all dependencies of a country by setting a single value and a timebin."),
        rpki_status: Optional[str] = Query(
            None, description="Route origin validation state for the monitored prefix and origin AS using RPKI."),
        irr_status: Optional[str] = Query(
            None, description="Route origin validation state for the monitored prefix and origin AS using IRR."),
        delegated_prefix_status: Optional[str] = Query(
            None, description="Status of the monitored prefix in the RIR's delegated stats. Status other than 'assigned' are usually considered as bogons."),
        delegated_asn_status: Optional[str] = Query(
            None, description="Status of the origin ASN in the RIR's delegated stats. Status other than 'assigned' are usually considered as bogons."),
        af: Optional[int] = Query(
            None, description="Address Family (IP version), values are either 4 or 6."),
        hege: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the monitored prefix. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        hege__gte: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the monitored prefix. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        hege__lte: Optional[float] = Query(
            None, description="AS Hegemony is the estimated fraction of paths towards the monitored prefix. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies."),
        origin_only: Optional[bool] = Query(
            None, description="Filter out dependency results and provide only prefix/origin ASN results"),
        page: Optional[int] = Query(
            1, ge=1, description="A page number within the paginated result set"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results")
    ) -> GenericResponseDTO[HegemonyPrefixDTO]:
        """
        List AS dependencies of prefixes. 
        <ul>
        <li><b>Required parameters:</b> timebin or a range of timebins (using the two parameters timebin__lte and timebin__gte). And one of the following: prefix, originasn, country, rpki_status, irr_status, delegated_prefix_status, delegated_asn_status.</li>
        <li><b>Limitations:</b> At most 3 days of data can be fetched per request. For bulk downloads see: <a href="https://archive.ihr.live/" target="_blank">https://archive.ihr.live/</a>.</li>
        </ul>
        """
        # Ensure at least one filter is provided
        if not any([prefix, originasn, country, rpki_status, irr_status,
                   delegated_prefix_status, delegated_asn_status]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Required parameter missing. Please provide one of the following parameter: ['prefix', 'originasn', 'country', 'rpki_status', 'irr_status', 'delegated_prefix_status', 'delegated_asn_status']"
            )

        timebin__gte, timebin__lte = validate_timebin_params(
            timebin, timebin__gte, timebin__lte, max_days=3)

        # Convert comma-separated values to lists
        prefix_list = [x.strip()
                       for x in prefix.split(",")] if prefix else None
        asn_list = [int(x.strip()) for x in asn.split(",")] if asn else None
        originasn_list = [int(x.strip())
                          for x in originasn.split(",")] if originasn else None
        country_list = [x.strip()
                        for x in country.split(",")] if country else None

        prefixes, total_count = HegemonyController.service.get_hegemony_prefixes(
            db,
            timebin_gte=timebin__gte,
            timebin_lte=timebin__lte,
            prefixes=prefix_list,
            asn_ids=asn_list,
            originasn_ids=originasn_list,
            countries=country_list,
            rpki_status=rpki_status,
            irr_status=irr_status,
            delegated_prefix_status=delegated_prefix_status,
            delegated_asn_status=delegated_asn_status,
            af=af,
            hege=hege,
            hege_gte=hege__gte,
            hege_lte=hege__lte,
            origin_only=origin_only,
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
            results=prefixes
        )
