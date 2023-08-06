from typing import TYPE_CHECKING

import numpy as np
from .._content_data_validator import ContentDataValidator
from ...._df_builder import build_dates_calendars_date_schedule_df
from .....content.ipa._content_provider import (
    DatesAndCalendarsDateScheduleRequestFactory,
)
from .....delivery._data._data_provider import (
    ResponseFactory,
    DataProvider,
    ValidatorContainer,
    Data,
)

if TYPE_CHECKING:
    from .....delivery._data._data_provider import ParsedData


class DateSchedule(Data):
    def __init__(self, raw: dict):
        super().__init__(raw, dfbuilder=build_dates_calendars_date_schedule_df)
        self._dates = []

    @property
    def dates(self):
        if self._dates:
            return self._dates

        dates = []
        for date in self.raw["dates"]:
            date = np.datetime64(date)
            dates.append(date)
        return dates


class DateScheduleResponseFactory(ResponseFactory):
    def create_success(
        self, data: "ParsedData", session: "Session" = None, **kwargs: dict
    ):
        response = self.response_class(True, data)
        response.data = DateSchedule(data.content_data)
        return response

    def create_fail(self, data: "ParsedData", **kwargs: dict):
        if data.status.get("error", {}).get("errors"):
            message = data.status["error"]["errors"][0]["reason"]
            data.error_messages = f"{data.first_error_message}. {message}"

        return super().create_fail(data, **kwargs)


date_schedule_data_provider = DataProvider(
    request=DatesAndCalendarsDateScheduleRequestFactory(),
    response=DateScheduleResponseFactory(),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
