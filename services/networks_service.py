from sqlalchemy.orm import Session
from repositories.networks_repository import NetworksRepository
from dtos.networks_dto import NetworksDTO
from typing import Optional, List, Tuple


class NetworksService:
    def __init__(self):
        self.repository = NetworksRepository()

    def get_networks(
        self,
        db: Session,
        name: Optional[str] = None,
        numbers: Optional[List[int]] = None,
        number_gte: Optional[int] = None,
        number_lte: Optional[int] = None,
        search: Optional[str] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[NetworksDTO], int]:
        """
        Get network data with various filtering options.
        """
        networks, total_count = self.repository.get_all(
            db,
            name=name,
            numbers=numbers,
            number_gte=number_gte,
            number_lte=number_lte,
            search=search,
            page=page,
            order_by=order_by
        )

        return [NetworksDTO.from_model(network) for network in networks], total_count
