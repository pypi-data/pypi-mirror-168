from itertools import product
from typing import List, Tuple, Dict

import pandas as pd
from pandas.core.tools.datetimes import DatetimeScalarOrArrayConvertible

from ._types import Strings
from .._tools._dataframe import convert_str_to_datetime


def historical_build_df_one_inst(
    raw: dict, fields: Strings, axis_name: str
) -> pd.DataFrame:
    inst_name = raw["universe"]["ric"]
    data, columns, index = process_historical_raw(raw, fields)
    columns = pd.Index(data=columns, name=inst_name)
    index = pd.Index(data=index, name=axis_name)
    df = pd.DataFrame(data=data, columns=columns, index=index)
    df.sort_index(inplace=True)
    return df


def process_by_fields(timestamp_index, listoflists, fields, headers_names):
    data = []
    index = []
    for l in listoflists:
        index.append(convert_str_to_datetime(l[timestamp_index]))
        newl = []
        for field in fields:
            if field in headers_names:
                item = l[headers_names.index(field)]
                newl.append(pd.NA if item is None else item)
            else:
                newl.append(pd.NA)
        data.append(newl)
    return data, fields, index


def process_by_headers_names(
    timestamp_index, timestamp_name, listoflists, headers_names
):
    data = []
    index = []
    for l in listoflists:
        newl = []
        for item, hdr_name in zip(l, headers_names):
            if timestamp_name == hdr_name:
                index.append(convert_str_to_datetime(item))
                continue
            newl.append(pd.NA if item is None else item)
        data.append(newl)
    headers_names.pop(timestamp_index)
    return data, headers_names, index


def process_historical_raw(
    raw: dict, fields: Strings
) -> Tuple[List[list], Strings, List[DatetimeScalarOrArrayConvertible]]:
    listoflists = raw["data"]
    headers = raw["headers"]
    headers_names = [header["name"] for header in headers]

    timestamp_name = None
    if "DATE_TIME" in headers_names:
        timestamp_name = "DATE_TIME"
    elif "DATE" in headers_names:
        timestamp_name = "DATE"

    timestamp_index = headers_names.index(timestamp_name)

    if fields:
        data, columns, index = process_by_fields(
            timestamp_index, listoflists, fields, headers_names
        )

    else:
        data, columns, index = process_by_headers_names(
            timestamp_index, timestamp_name, listoflists, headers_names
        )

    return data, columns, index


def prepare_columns(
    raws, listofcolumns, bad_raws, fields, universe, items_by_date, num_fields
):
    raw_columns = None
    listofcolumns_append = listofcolumns.append
    bad_raws_append = bad_raws.append

    for instidx, raw in enumerate(raws):
        # it means error in response for custom instruments
        if not raw:
            raw = {"universe": {"ric": universe[instidx]}}
            bad_raws_append((instidx, raw))
            continue

        # it means error in response for historical pricing
        if isinstance(raw, list):
            raw = raw[0]
            bad_raws_append((instidx, raw))
            continue

        else:
            raw_datas, raw_columns, raw_index = process_historical_raw(raw, fields)

        for date, raw_data in zip(raw_index, raw_datas):
            items = items_by_date.setdefault(date, [])
            items.append((instidx, raw_data, raw_columns))

        inst_name = raw["universe"]["ric"]
        if num_fields == 1:
            processed_columns = [inst_name]

        else:
            processed_columns = list(product([inst_name], raw_columns))

        listofcolumns_append(processed_columns)

    return raw_columns


def process_bad_raws(bad_raws, listofcolumns, last_raw_columns, fields, num_fields):
    listofcolumns_insert = listofcolumns.insert

    for idx, bad_raw in bad_raws:
        raw_columns = fields or last_raw_columns or "Field"
        inst_name = bad_raw["universe"]["ric"]
        if num_fields == 1:
            processed_columns = [inst_name]

        else:
            processed_columns = list(product([inst_name], raw_columns))

        listofcolumns_insert(idx, processed_columns)


def process_data(
    data_append, index_append, date, items, num_allcolumns, num_raws, left_num_columns
):
    prev_idx = None
    counter = 0

    template = [pd.NA] * num_allcolumns
    for instidx, raw_data, raw_columns in items:
        if (counter != 0 and counter % num_raws == 0) or prev_idx == instidx:
            index_append(date)
            data_append(template)
            template = [pd.NA] * num_allcolumns
            prev_idx = instidx

        if prev_idx is None:
            prev_idx = instidx

        counter += 1

        left_idx = left_num_columns[instidx]
        right_idx = left_idx + len(raw_columns)
        for item, i in zip(raw_data, range(left_idx, right_idx)):
            template[i] = item

    index_append(date)
    data_append(template)


def historical_build_df_multi_inst(
    raws: List[dict], universe: Strings, fields: Strings, axis_name: str
) -> pd.DataFrame:
    items_by_date: Dict[str, list] = {}
    listofcolumns = []
    num_raws = len(raws)
    bad_raws = []
    num_fields = len(fields)

    last_raw_columns = prepare_columns(
        raws, listofcolumns, bad_raws, fields, universe, items_by_date, num_fields
    )

    if bad_raws:
        process_bad_raws(bad_raws, listofcolumns, last_raw_columns, fields, num_fields)

    left_num_columns = {
        split_idx: sum([len(subcols) for subcols in listofcolumns[:split_idx]])
        for split_idx in range(num_raws)
    }

    allcolumns = [col for subcolumns in listofcolumns for col in subcolumns]

    num_allcolumns = len(allcolumns)
    data = []
    index = []
    data_append = data.append
    index_append = index.append
    for date, items in items_by_date.items():

        num_items = len(items)

        if num_items > 1:
            process_data(
                data_append,
                index_append,
                date,
                items,
                num_allcolumns,
                num_raws,
                left_num_columns,
            )

        else:
            index_append(date)
            instidx, raw_data, raw_columns = items[0]
            left = [pd.NA] * left_num_columns[instidx]
            right = [pd.NA] * (num_allcolumns - len(raw_columns) - len(left))
            data_append(left + raw_data + right)

    if num_fields == 1:
        columns = pd.Index(data=allcolumns, name=fields[0])

    else:
        columns = pd.MultiIndex.from_tuples(allcolumns)

    index = pd.Index(data=index, name=axis_name)
    df = pd.DataFrame(data=data, columns=columns, index=index)
    df.sort_index(inplace=True)
    return df
