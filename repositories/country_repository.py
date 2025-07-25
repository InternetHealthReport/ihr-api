from sqlalchemy.orm import Session
from models.country import Country
from typing import Optional, List, Tuple  # Added Tuple for return type
from sqlalchemy import asc
from utils import page_size


class CountryRepository:
    def get_all(
        self,
        db: Session,
        code: Optional[str] = None,
        name: Optional[str] = None,
        page: int = 1,            # Page number, defaults to 1
        order_by: Optional[str] = None,  # Column name to sort by
    ) -> Tuple[List[Country], int]:      # Returns list of countries and total count
        """
        Retrieves countries with pagination and ordering at database level.
        Returns: Tuple[List[Country], total_count]
        """
        # Initialize base query
        query = db.query(Country)

        # Apply filters if provided
        if code:
            query = query.filter(Country.code == code)
        if name:
            query = query.filter(Country.name.ilike(f"%{name}%"))

        # Executes getting total count of countries
        total_count = query.count()

        # Apply ordering if specified
        if order_by and hasattr(Country, order_by):
            query = query.order_by(asc(getattr(Country, order_by)))

        # Calculate offset based on page number and size
        offset = (page - 1) * page_size
        # Apply pagination and execute query
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
