from sqlalchemy.orm import Session
from sqlalchemy import or_, String
from models.asn import ASN
from typing import Optional, List, Tuple
from utils import page_size


class NetworksRepository:
    def get_all(
        self,
        db: Session,
        name: Optional[str] = None,
        numbers: Optional[List[int]] = None,
        number_gte: Optional[int] = None,
        number_lte: Optional[int] = None,
        search: Optional[str] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[ASN], int]:
        query = db.query(ASN)

        # Apply filters
        if name:
            query = query.filter(ASN.name.ilike(f"%{name}%"))
        if numbers:
            query = query.filter(ASN.number.in_(numbers))
        if number_gte:
            query = query.filter(ASN.number >= number_gte)
        if number_lte:
            query = query.filter(ASN.number <= number_lte)
        if search:
            # Handle AS/IX prefix in search
            search_value = search
            if search.upper().startswith(("AS", "IX")):
                try:
                    search_value = str(int(search[2:]))
                except ValueError:
                    pass

            query = query.filter(or_(
                ASN.number.cast(String).contains(search_value),
                ASN.name.ilike(f"%{search}%")
            ))

        total_count = query.count()

        # Apply ordering
        if order_by and hasattr(ASN, order_by):
            query = query.order_by(getattr(ASN, order_by))

        # Apply pagination
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
