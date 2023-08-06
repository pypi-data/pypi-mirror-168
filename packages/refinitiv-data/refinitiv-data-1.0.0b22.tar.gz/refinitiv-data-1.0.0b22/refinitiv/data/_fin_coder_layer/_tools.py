from typing import List

import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_datetime64_any_dtype

from .._tools import custom_convert_dtypes


def get_name_columns_without_datetime(df: pd.DataFrame) -> List[str]:
    return [
        column_name
        for column_name, dtype in df.dtypes.to_dict().items()
        if not is_datetime64_any_dtype(dtype)
    ]


def working_with_missing_data_and_convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    df.fillna(np.nan, inplace=True)
    df = custom_convert_dtypes(df)
    df.fillna(pd.NA, inplace=True)
    return df
