from sqlalchemy.orm import Session
from repositories.country_repository import CountryRepository
from dtos.country_dto import CountryDTO
from typing import Optional, List, Tuple


class CountryService:
    def __init__(self):
        self.repository = CountryRepository()

    def get_all_countries(
        self,
        db: Session,
        code: Optional[str] = None,
        name: Optional[str] = None,
        page: int = 1,                 # Page number, defaults to 1
        order_by: Optional[str] = None # Column name to sort by
    ) -> Tuple[List[CountryDTO], int]:
        """Fetches paginated countries, applying filters if provided."""

        countries, total_count = self.repository.get_all(
            db,
            code=code,
            name=name,
            page=page,
            order_by=order_by   
        )
        return [CountryDTO(code=c.code, name=c.name) for c in countries], total_count
