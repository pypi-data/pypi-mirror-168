import datetime
from typing import List, Optional, Union
from ...content.ipa.dates_and_calendars.is_working_day import Definition


def is_working_day(
    date: Union[str, datetime.date, datetime.datetime, datetime.timedelta],
    currencies: Optional[List[str]] = None,
    calendars: Optional[List[str]] = None,
) -> bool:
    response = Definition(
        date=date, calendars=calendars, currencies=currencies
    ).get_data()

    return response.data.day.is_working_day
