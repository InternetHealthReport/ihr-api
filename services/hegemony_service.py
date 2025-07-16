from sqlalchemy.orm import Session
from repositories.hegemony_cone_repository import HegemonyConeRepository
from dtos.hegemony_cone_dto import HegemonyConeDTO
from repositories.hegemony_alarms_repository import HegemonyAlarmsRepository
from dtos.hegemony_alarms_dto import HegemonyAlarmsDTO
from repositories.hegemony_country_repository import HegemonyCountryRepository
from dtos.hegemony_country_dto import HegemonyCountryDTO
from repositories.hegemony_repository import HegemonyRepository
from dtos.hegemony_dto import HegemonyDTO
from repositories.hegemony_prefix_repository import HegemonyPrefixRepository
from dtos.hegemony_prefix_dto import HegemonyPrefixDTO
from typing import Optional, List, Tuple
from datetime import datetime


class HegemonyService:
    def __init__(self):
        self.hegemony_cone_repository = HegemonyConeRepository()
        self.hegemony_alarms_repository = HegemonyAlarmsRepository()
        self.hegemony_country_repository = HegemonyCountryRepository()
        self.hegemony_repository = HegemonyRepository()
        self.hegemony_prefix_repository = HegemonyPrefixRepository()

    def get_hegemony_cones(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        af: Optional[int] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[HegemonyConeDTO], int]:
        """
        Get hegemony cone data with time-based filtering.
        """
        cones, total_count = self.hegemony_cone_repository.get_all(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            asn_ids=asn_ids,
            af=af,
            page=page,
            order_by=order_by
        )

        return [HegemonyConeDTO(
            timebin=cone.timebin,
            asn=cone.asn,
            conesize=cone.conesize,
            af=cone.af
        ) for cone in cones], total_count

    def get_hegemony_alarms(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        originasn_ids: Optional[List[int]] = None,
        af: Optional[int] = None,
        deviation_gte: Optional[float] = None,
        deviation_lte: Optional[float] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[HegemonyAlarmsDTO], int]:
        """
        Get hegemony alarms data with filtering.
        """
        alarms, total_count = self.hegemony_alarms_repository.get_all(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            asn_ids=asn_ids,
            originasn_ids=originasn_ids,
            af=af,
            deviation_gte=deviation_gte,
            deviation_lte=deviation_lte,
            page=page,
            order_by=order_by
        )

        return [HegemonyAlarmsDTO(
            timebin=alarm.timebin,
            originasn=alarm.originasn,
            asn=alarm.asn,
            deviation=alarm.deviation,
            af=alarm.af,
            asn_name=alarm.asn_relation.name if alarm.asn_relation else None,
            originasn_name=alarm.originasn_relation.name if alarm.originasn_relation else None
        ) for alarm in alarms], total_count

    def get_hegemony_countries(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        countries: Optional[List[str]] = None,
        af: Optional[int] = None,
        weightscheme: Optional[str] = None,
        transitonly: Optional[bool] = None,
        hege: Optional[float] = None,
        hege_gte: Optional[float] = None,
        hege_lte: Optional[float] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[HegemonyCountryDTO], int]:
        """
        Get hegemony country data with filtering.
        """
        countries_data, total_count = self.hegemony_country_repository.get_all(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            asn_ids=asn_ids,
            countries=countries,
            af=af,
            weightscheme=weightscheme,
            transitonly=transitonly,
            hege=hege,
            hege_gte=hege_gte,
            hege_lte=hege_lte,
            page=page,
            order_by=order_by
        )

        return [HegemonyCountryDTO(
            timebin=country.timebin,
            country=country.country,
            asn=country.asn,
            hege=country.hege,
            af=country.af,
            asn_name=country.asn_relation.name if country.asn_relation else None,
            weight=country.weight,
            weightscheme=country.weightscheme,
            transitonly=country.transitonly
        ) for country in countries_data], total_count

    def get_hegemony(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        asn_ids: Optional[List[int]] = None,
        originasn_ids: Optional[List[int]] = None,
        af: Optional[int] = None,
        hege: Optional[float] = None,
        hege_gte: Optional[float] = None,
        hege_lte: Optional[float] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[HegemonyDTO], int]:
        """
        Get hegemony data with filtering.
        """
        hegemony_data, total_count = self.hegemony_repository.get_all(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            asn_ids=asn_ids,
            originasn_ids=originasn_ids,
            af=af,
            hege=hege,
            hege_gte=hege_gte,
            hege_lte=hege_lte,
            page=page,
            order_by=order_by
        )

        return [HegemonyDTO(
            timebin=hegemony.timebin,
            originasn=hegemony.originasn,
            asn=hegemony.asn,
            hege=hegemony.hege,
            af=hegemony.af,
            asn_name=hegemony.asn_relation.name if hegemony.asn_relation else None,
            originasn_name=hegemony.originasn_relation.name if hegemony.originasn_relation else None
        ) for hegemony in hegemony_data], total_count

    def get_hegemony_prefixes(
        self,
        db: Session,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        prefixes: Optional[List[str]] = None,
        asn_ids: Optional[List[int]] = None,
        originasn_ids: Optional[List[int]] = None,
        countries: Optional[List[str]] = None,
        rpki_status: Optional[str] = None,
        irr_status: Optional[str] = None,
        delegated_prefix_status: Optional[str] = None,
        delegated_asn_status: Optional[str] = None,
        af: Optional[int] = None,
        hege: Optional[float] = None,
        hege_gte: Optional[float] = None,
        hege_lte: Optional[float] = None,
        origin_only: Optional[bool] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[HegemonyPrefixDTO], int]:
        """
        Get hegemony prefix data with filtering.
        """
        prefixes_data, total_count = self.hegemony_prefix_repository.get_all(
            db,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            prefixes=prefixes,
            asn_ids=asn_ids,
            originasn_ids=originasn_ids,
            countries=countries,
            rpki_status=rpki_status,
            irr_status=irr_status,
            delegated_prefix_status=delegated_prefix_status,
            delegated_asn_status=delegated_asn_status,
            af=af,
            hege=hege,
            hege_gte=hege_gte,
            hege_lte=hege_lte,
            origin_only=origin_only,
            page=page,
            order_by=order_by
        )

        return [HegemonyPrefixDTO(
            timebin=prefix.timebin,
            prefix=prefix.prefix,
            originasn=prefix.originasn,
            country=prefix.country,
            asn=prefix.asn,
            hege=prefix.hege,
            af=prefix.af,
            visibility=prefix.visibility,
            rpki_status=prefix.rpki_status,
            irr_status=prefix.irr_status,
            delegated_prefix_status=prefix.delegated_prefix_status,
            delegated_asn_status=prefix.delegated_asn_status,
            descr=prefix.descr,
            moas=prefix.moas,
            originasn_name=prefix.originasn_relation.name if prefix.originasn_relation else None,
            asn_name=prefix.asn_relation.name if prefix.asn_relation else None
        ) for prefix in prefixes_data], total_count
