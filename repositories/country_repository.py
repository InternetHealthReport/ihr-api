from sqlalchemy.orm import Session
from sqlalchemy import select, func, asc
from models.country import Country
from typing import Optional, List, Tuple
from utils import page_size


class CountryRepository:
    def get_all(
        self,
        db: Session,
        code: Optional[str] = None,
        name: Optional[str] = None,
        page: int = 1,
        order_by: Optional[str] = None,
    ) -> Tuple[List[Country], int]:
        stmt = select(Country)

        if code:
            stmt = stmt.where(Country.code == code)
        if name:
            stmt = stmt.where(Country.name.ilike(f"%{name}%"))

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        if order_by and hasattr(Country, order_by):
            stmt = stmt.order_by(asc(getattr(Country, order_by)))

        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).all()

        return results, total_count
