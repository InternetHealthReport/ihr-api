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

    if (not timebin_gte and timebin_lte) or (timebin_gte and not timebin_lte):
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