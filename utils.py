from typing import Optional, Tuple
from datetime import datetime, timedelta, date
from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
try:
    load_dotenv()
except:
    pass

page_size = int(os.getenv("PAGE_SIZE"))

def validate_timebin_params(
    timebin: Optional[datetime],
    timebin_gte: Optional[datetime],
    timebin_lte: Optional[datetime],
    max_days: int = 7
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

    # Validate date range based on max_days parameter
    if timebin_gte and timebin_lte:
        delta = timebin_lte - timebin_gte
        if delta > timedelta(days=max_days):
            raise HTTPException(
                status_code=400,
                detail=f"The given timebin range is too large. Should be less than {max_days} days."
            )

    return timebin_gte, timebin_lte


def prepare_timebin_range(
    timebin: Optional[datetime],
    timebin_gte: Optional[datetime],
    timebin_lte: Optional[datetime],
    max_days: int = 7
) -> Tuple[datetime, Optional[datetime]]:

    if (not timebin_gte and timebin_lte) or (timebin_gte and not timebin_lte):
        raise HTTPException(
            status_code=400,
            detail="Invalid timebin range. Please provide both timebin__lte and timebin__gte."
        )
    # If no time filters provided, default to last 6 days (including today)
    if not any([timebin, timebin_gte, timebin_lte]):
        today = datetime.combine(date.today(), datetime.min.time())
        timebin_gte = today - timedelta(days=6)

    # Validate range size if both are given
    if timebin_gte and timebin_lte:
        delta = timebin_lte - timebin_gte
        if delta > timedelta(days=max_days):
            raise HTTPException(
                status_code=400,
                detail=f"The given timebin range is too large. Should be less than {max_days} days."
            )

    return timebin_gte, timebin_lte
