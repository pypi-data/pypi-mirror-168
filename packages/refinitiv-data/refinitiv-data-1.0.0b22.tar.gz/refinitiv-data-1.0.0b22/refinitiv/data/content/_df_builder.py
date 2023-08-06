import abc
from copy import deepcopy
from functools import partial
from itertools import product
from typing import List, Optional, Any, Set

import pandas as pd

from .._tools._dataframe import convert_str_to_datetime


def partial_process_index(
    num_unique_insts,
    num_columns,
    fields_by_inst_by_date,
    index,
    unique_insts,
    inst,
    date_str,
    fields,
):
    is_add = True

    if num_unique_insts > 1:
        total = num_unique_insts * num_columns
        template = [pd.NA] * total

        idx = unique_insts.index(inst)
        right_idx = idx * num_columns + num_columns
        left_idx = idx * num_columns
        for item, idx in zip(fields, range(left_idx, right_idx)):
            template[idx] = item
        fields = template

        fields_by_inst = fields_by_inst_by_date.get(date_str)
        if fields_by_inst and inst not in fields_by_inst.keys():
            is_add = False
            idx = max(unique_insts.index(inst) for inst in fields_by_inst.keys())
            cache_inst = unique_insts[idx]
            cache_fields = fields_by_inst[cache_inst]
            idx = unique_insts.index(inst)
            cache_idx = unique_insts.index(cache_inst)

            left_idx = cache_idx * num_columns + num_columns
            right_idx = idx * num_columns + num_columns

            for idx in range(left_idx, right_idx):
                cache_fields[idx] = fields[idx]

            fields_by_inst[inst] = cache_fields
            fields = cache_fields

        else:
            not fields_by_inst and fields_by_inst_by_date.setdefault(
                date_str, {inst: fields}
            )
            date = convert_str_to_datetime(date_str)
            index.append(date)

    else:
        date = convert_str_to_datetime(date_str)
        index.append(date)

    return fields, is_add


class DFBuilder(abc.ABC):
    auto_headers: Optional[List] = None

    @abc.abstractmethod
    def get_headers(self, content_data: dict) -> List[dict]:
        # for override
        pass

    def get_date_idxs(self, columns: List[str]) -> Set[int]:
        return {idx for idx, col in enumerate(columns) if "date" in col.lower()}

    def build_index(
        self, content_data: dict, use_field_names_in_headers: bool = False, **kwargs
    ) -> pd.DataFrame:

        key = "name" if use_field_names_in_headers else "title"

        headers = self.get_headers(content_data)
        columns = [header[key] for header in headers]
        date_idxs = self.get_date_idxs(columns)

        data = []
        fields_list = content_data.get("data", [])
        for fields in fields_list:
            fields = list(fields)

            for idx, item in enumerate(fields):
                if item is None:
                    fields[idx] = pd.NA

            for idx in date_idxs:
                fields[idx] = convert_str_to_datetime(fields[idx])

            data.append(fields)

        df = pd.DataFrame(data=data, columns=columns)
        return df

    def build_date_as_index(
        self,
        content_data: dict,
        use_field_names_in_headers: bool = False,
        use_multiindex: bool = False,
        **kwargs,
    ) -> pd.DataFrame:
        key = "name" if use_field_names_in_headers else "title"

        headers = self.get_headers(content_data)
        columns = [header[key] for header in headers]

        inst_header, date_header = self.auto_headers
        inst_header = inst_header[key]
        date_header = date_header[key]

        data = []
        index = []
        inst_idx = columns.index(inst_header)
        date_idx = columns.index(date_header)
        columns.pop(date_idx)
        columns.pop(inst_idx)
        num_columns = len(columns)

        date_idxs = self.get_date_idxs(columns)
        fields_by_inst_by_date = {}
        fields_list = content_data.get("data", [])
        unique_insts = list(dict.fromkeys(fields[inst_idx] for fields in fields_list))
        num_unique_insts = len(unique_insts)
        process_index = partial(
            partial_process_index,
            num_unique_insts,
            num_columns,
            fields_by_inst_by_date,
            index,
            unique_insts,
        )
        for fields in fields_list:
            fields = list(fields)
            date_str = fields[date_idx]

            if not date_str:
                continue

            inst = fields[inst_idx]
            fields.pop(date_idx)
            fields.pop(inst_idx)

            for idx, item in enumerate(fields):
                if item is None:
                    fields[idx] = pd.NA

            for idx in date_idxs:
                fields[idx] = convert_str_to_datetime(fields[idx])

            fields, is_add = process_index(inst, date_str, fields)

            is_add and data.append(fields)

        if num_unique_insts > 1 or use_multiindex:
            columns = pd.MultiIndex.from_tuples(product(unique_insts, columns))

        elif num_unique_insts == 1:
            columns = pd.Index(data=columns, name=unique_insts.pop())

        index = pd.Index(data=index, name=date_header)
        df = pd.DataFrame(data=data, columns=columns, index=index)
        df.sort_index(ascending=False, inplace=True)
        return df


class DFBuilderRDP(DFBuilder):
    """
    {
        "links": {"count": 2},
        "variability": "",
        "universe": [
            {
                "Instrument": "GOOG.O",
                "Company Common Name": "Alphabet Inc",
                "Organization PermID": "5030853586",
                "Reporting Currency": "USD",
            }
        ],
        "data": [
            ["GOOG.O", "2022-01-26T00:00:00", "USD", None],
            ["GOOG.O", "2020-12-31T00:00:00", None, "2020-12-31T00:00:00"],
        ],
        "messages": {
            "codes": [[-1, -1, -1, -2], [-1, -1, -2, -1]],
            "descriptions": [
                {"code": -2, "description": "empty"},
                {"code": -1, "description": "ok"},
            ],
        },
        "headers": [
            {
                "name": "instrument",
                "title": "Instrument",
                "type": "string",
                "description": "The requested Instrument as defined by the user.",
            },
            {
                "name": "date",
                "title": "Date",
                "type": "datetime",
                "description": "Date associated with the returned data.",
            },
            {
                "name": "TR.RevenueMean",
                "title": "Currency",
                "type": "string",
                "description": "The statistical average of all broker ...",
            },
            {
                "name": "TR.Revenue",
                "title": "Date",
                "type": "datetime",
                "description": "Is used for industrial and utility companies. ...",
            },
        ],
    }
    """

    auto_headers = [
        {"name": "instrument", "title": "Instrument"},
        {"name": "date", "title": "Date"},
    ]

    def get_headers(self, content_data) -> List[dict]:
        return content_data.get("headers", [])


class DFBuilderUDF(DFBuilder):
    """
    {
        "columnHeadersCount": 1,
        "data": [
            ["GOOG.O", "2022-01-26T00:00:00Z", "USD", ""],
            ["GOOG.O", "2020-12-31T00:00:00Z", "", "2020-12-31T00:00:00Z"],
        ],
        "headerOrientation": "horizontal",
        "headers": [
            [
                {"displayName": "Instrument"},
                {"displayName": "Date"},
                {"displayName": "Currency", "field": "TR.REVENUEMEAN.currency"},
                {"displayName": "Date", "field": "TR.REVENUE.DATE"},
            ]
        ],
        "rowHeadersCount": 2,
        "totalColumnsCount": 4,
        "totalRowsCount": 3,
    }
    """

    auto_headers = [
        {"name": "Instrument", "title": "Instrument"},
        {"name": "Date", "title": "Date"},
    ]

    def get_headers(self, content_data) -> List[dict]:
        headers = content_data["headers"]
        headers = headers[0]
        return [
            {
                "name": header.get("field") or header.get("displayName"),
                "title": header.get("displayName"),
            }
            for header in headers
        ]


def build_dates_calendars_df(raw: Any, **kwargs):
    raw = deepcopy(raw)
    add_periods_data = []

    clean_request_items = []
    for item in raw:
        if not item.get("error"):
            clean_request_items.append(item)

    for request_item in clean_request_items:
        if request_item.get("date"):
            request_item["date"] = convert_str_to_datetime(request_item["date"])

        request_item.pop("holidays", None)
        add_periods_data.append(request_item)

    _df = pd.DataFrame(add_periods_data)

    return _df


def build_dates_calendars_holidays_df(raw: Any, **kwargs):
    holidays_data = _dates_calendars_prepare_holidays_data(raw)
    holidays_df = pd.DataFrame(holidays_data)
    return holidays_df


def _dates_calendars_prepare_holidays_data(raw):
    raw = deepcopy(raw)
    holidays_data = []

    for request_item_holiday in raw:
        for holiday in request_item_holiday.get("holidays", []):
            if holiday.get("names"):
                for holiday_name in holiday["names"]:
                    holiday_name["tag"] = request_item_holiday.get("tag")
                    holiday_name["date"] = convert_str_to_datetime(holiday.get("date"))
                    holidays_data.append(holiday_name)
            else:
                holiday["tag"] = request_item_holiday.get("tag")
                holidays_data.append(holiday)
    return holidays_data


def default_build_df(raw: Any, **kwargs) -> pd.DataFrame:
    df = pd.DataFrame(raw)
    return df


def build_dates_calendars_date_schedule_df(raw: Any, **kwargs) -> pd.DataFrame:
    raw = deepcopy(raw)

    _dates = []
    for date in raw.get("dates"):
        _dates.append(convert_str_to_datetime(date))

    raw["dates"] = _dates
    df = pd.DataFrame(raw)
    return df


def build_empty_df(*args, **kwargs) -> pd.DataFrame:
    return pd.DataFrame()


dfbuilder_rdp = DFBuilderRDP()
dfbuilder_udf = DFBuilderUDF()
