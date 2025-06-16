from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from services.country_service import CountryService
from dtos.generic_response_dto import GenericResponseDTO, build_url
from dtos.country_dto import CountryDTO
from config.database import get_db
from typing import Optional
from globals import page_size

# Define a router for all endpoints under /countries
router = APIRouter(prefix="/countries", tags=["Countries"])


class CountryController:
    service = CountryService()

    @staticmethod
    @router.get("/", response_model=GenericResponseDTO[CountryDTO])
    def get_all_countries(
        request: Request,
        db: Session = Depends(get_db),
        page: Optional[int] = Query(
            None, ge=1, description="A page number within the paginated result set"),
        code: Optional[str] = Query(
            None, description="Search by country code"),
        name: Optional[str] = Query(
            None, description="Search for a substring in countries name"),
        ordering: Optional[str] = Query(
            None, description="Which field to use when ordering the results")
    ) -> GenericResponseDTO[CountryDTO]:
        """Retrieves paginated countries with optional filters."""
       
        page = page or 1
        countries, total_count = CountryController.service.get_all_countries(
            db,
            code=code,
            name=name,
            page=page,
            order_by=ordering
        )

        # Calculate next and previous pages
        next_page = page + 1 if (page * page_size) < total_count else None
        prev_page = page - 1 if page > 1 else None

        return GenericResponseDTO(
            count=total_count,
            next=build_url(request, next_page),
            previous=build_url(request, prev_page),
            results=countries
        )
