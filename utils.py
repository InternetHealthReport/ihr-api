from fastapi import  HTTPException
from datetime import datetime, timedelta
from typing import Optional


def validate_timebin_params(
        timebin: Optional[datetime],
        timebin_gte: Optional[datetime],
        timebin_lte: Optional[datetime]
    ) -> tuple[datetime, datetime]:
       
        # Check if at least one time parameter exists
        if not any([timebin, timebin_gte, timebin_lte]):
            raise HTTPException(
                status_code=400,
                detail="No timebin parameter. Please provide a timebin value or a range of values with timebin__lte and timebin__gte."
            )

        # If timebin is not provided, both timebin_gte and timebin_lte must be provided
        if not timebin and not (timebin_gte and timebin_lte):
            raise HTTPException(
                status_code=400,
                detail="Invalid timebin range. Please provide both timebin__lte and timebin__gte."
            )

        # If exact timebin is provided, it overrides the range parameters
        if timebin:
            timebin_gte = timebin
            timebin_lte = timebin

        # Validate date range (max 7 days)
        if timebin_gte and timebin_lte:
            delta = timebin_lte - timebin_gte
            if delta > timedelta(days=7):
                raise HTTPException(
                    status_code=400,
                    detail="The given timebin range is too large. Should be less than 7 days."
                )

        return timebin_gte, timebin_lte
