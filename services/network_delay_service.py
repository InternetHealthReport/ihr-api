from sqlalchemy.orm import Session
from repositories.atlas_location_repository import AtlasLocationRepository
from repositories.atlas_delay_repository import AtlasDelayRepository
from dtos.network_delay_locations_dto import NetworkDelayLocationsDTO
from dtos.network_delay_dto import NetworkDelayDTO
from typing import Optional, List, Tuple
from datetime import datetime


class NetworkDelayService:
    def __init__(self):
        self.atlas_location_repository = AtlasLocationRepository()
        self.atlas_delay_repository = AtlasDelayRepository()

    def get_network_delay_locations(
        self,
        db: Session,
        name: Optional[str] = None,
        type: Optional[str] = None,
        af: Optional[int] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[NetworkDelayLocationsDTO], int]:
        """
        Get locations monitored for network delay measurements.
        """
        locations, total_count = self.atlas_location_repository.get_all(
            db,
            name=name,
            type=type,
            af=af,
            page=page,
            order_by=order_by
        )

        return [NetworkDelayLocationsDTO(
            type=location.type,
            name=location.name,
            af=location.af
        ) for location in locations], total_count

    def get_network_delays(
        self,
        db: Session,
        timebin: Optional[datetime] = None,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        startpoint_names: Optional[str] = None,
        endpoint_names: Optional[str] = None,
        startpoint_type: Optional[str] = None,
        endpoint_type: Optional[str] = None,
        startpoint_af: Optional[int] = None,
        endpoint_af: Optional[int] = None,
        median: Optional[float] = None,
        median_gte: Optional[float] = None,
        median_lte: Optional[float] = None,
        startpoint_key: Optional[str] = None,
        endpoint_key: Optional[str] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[NetworkDelayDTO], int]:
        """
        Get network delays with all possible filters.
        """
        atlasDelays, total_count = self.atlas_delay_repository.get_delays(
            db,
            timebin=timebin,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            startpoint_names=startpoint_names,
            endpoint_names=endpoint_names,
            startpoint_type=startpoint_type,
            endpoint_type=endpoint_type,
            startpoint_af=startpoint_af,
            endpoint_af=endpoint_af,
            median=median,
            median_gte=median_gte,
            median_lte=median_lte,
            startpoint_key=startpoint_key,
            endpoint_key=endpoint_key,
            page=page,
            order_by=order_by
        )

        return [NetworkDelayDTO.from_model(atlasDelay) for atlasDelay in atlasDelays], total_count
