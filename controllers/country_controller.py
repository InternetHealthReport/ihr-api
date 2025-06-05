from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from services.country_service import CountryService
from utils.pagination import PaginatedResponse, paginate_and_order
from dtos.country_dto import CountryDTO
from config.database import get_db
from typing import Optional
from dtos.pagination_dto import PaginationParams


router = APIRouter(prefix="/countries", tags=["Countries"])


class CountryController:
    service = CountryService()

    @staticmethod
    @router.get("/", response_model=PaginatedResponse[CountryDTO])
    def get_all_countries(
        request: Request,
        db: Session = Depends(get_db),
        pagination: PaginationParams = Depends(),  # Generic pagination params
        code: Optional[str] = Query(
            None, description="Filter by country code"),
        name: Optional[str] = Query(
            None, description="Search by country name (substring)")
    ):
        """Retrieves all countries with optional filters."""
        countries = CountryController.service.get_all_countries(
            db, code=code, name=name)
        return paginate_and_order(countries, request, pagination.page, pagination.ordering)
