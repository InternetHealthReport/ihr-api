from sqlalchemy.orm import Session
from repositories.country_repository import CountryRepository
from dtos.country_dto import CountryDTO
from typing import Optional, List


class CountryService:
    def __init__(self):
        self.repository = CountryRepository()

    def get_all_countries(self, db: Session, code: Optional[str] = None, name: Optional[str] = None) -> List[CountryDTO]:
        """Fetches all countries, applying filters if provided."""
        countries = self.repository.get_all(db, code, name)
        return [CountryDTO(code=c.code, name=c.name) for c in countries]
