import numpy as np
from datetime import date, datetime, timedelta
from typing import List, Optional, Union
from ...content.ipa._enums import DateMovingConvention, EndOfMonthConvention
from ...content.ipa.dates_and_calendars.add_periods import Definition


def add_periods(
    start_date: Union[str, date, datetime, timedelta],
    period: str,
    calendars: Optional[List[str]] = None,
    currencies: Optional[List[str]] = None,
    date_moving_convention: Optional[Union[DateMovingConvention, str]] = None,
    end_of_month_convention: Optional[Union[EndOfMonthConvention, str]] = None,
) -> np.datetime64:
    response = Definition(
        start_date=start_date,
        period=period,
        calendars=calendars,
        currencies=currencies,
        date_moving_convention=date_moving_convention,
        end_of_month_convention=end_of_month_convention,
    ).get_data()

    return np.datetime64(response.data.added_period.date)
