from sqlalchemy.orm import Session
from models.country_model import Country
from typing import Optional, List


class CountryRepository:
    def get_all(self, db: Session, code: Optional[str] = None, name: Optional[str] = None) -> List[Country]:
        """Retrieves countries, optionally filtering by code and name substring."""
        query = db.query(Country)

        if code:
            query = query.filter(Country.code == code)

        if name:
            query = query.filter(Country.name.ilike(f"%{name}%"))

        return query.all()
