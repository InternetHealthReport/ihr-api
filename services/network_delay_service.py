from sqlalchemy.orm import Session
from repositories.atlas_location_repository import AtlasLocationRepository
from dtos.network_delay_locations_dto import NetworkDelayLocationsDTO
from typing import Optional, List, Tuple


class NetworkDelayService:
    def __init__(self):
        self.atlas_location_repository = AtlasLocationRepository()

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
