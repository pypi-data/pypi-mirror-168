from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List, Optional, Union
from ...content.ipa._enums import PeriodType, DayCountBasis
from ...content.ipa.dates_and_calendars.count_periods import Definition


@dataclass
class CountedPeriods:
    count: float
    tenor: str


def count_periods(
    start_date: Union[str, date, datetime, timedelta],
    end_date: Union[str, date, datetime, timedelta],
    period_type: Optional[Union[PeriodType, str]] = None,
    calendars: Optional[List[str]] = None,
    currencies: Optional[List[str]] = None,
    day_count_basis: Optional[Union[DayCountBasis, str]] = None,
) -> CountedPeriods:
    response = Definition(
        start_date=start_date,
        end_date=end_date,
        period_type=period_type,
        calendars=calendars,
        currencies=currencies,
        day_count_basis=day_count_basis,
    ).get_data()

    response = CountedPeriods(
        response.data.counted_period.count, response.data.counted_period.tenor
    )

    return response
