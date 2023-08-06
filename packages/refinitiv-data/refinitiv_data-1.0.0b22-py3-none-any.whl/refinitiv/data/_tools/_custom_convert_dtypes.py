__all__ = ("custom_convert_dtypes",)

########################################################################################
# pandas = 1.3.5
# numpy = 1.22.2
# scipy = 1.8.0
########################################################################################


import numpy as np
import pandas as pd
from pandas import concat, Series
from pandas.core.generic import bool_t
from pandas._libs import lib
from pandas.core.dtypes.missing import notna

from pandas.core.dtypes.common import (
    is_bool_dtype,
    is_integer_dtype,
    is_numeric_dtype,
    is_object_dtype,
    is_string_dtype,
    pandas_dtype,
)

from pandas._typing import (
    FrameOrSeries,
    ArrayLike,
    DtypeObj,
)

_NUMBER_TYPE_MAP = {
    "mixed": pandas_dtype("Float64"),
    "mixed-integer": pandas_dtype("Int64"),
    "mixed-integer-float": pandas_dtype("Float64"),
}


def custom_convert_dtypes(
    obj: FrameOrSeries,
    infer_objects: bool_t = True,
    convert_string: bool_t = True,
    convert_integer: bool_t = True,
    convert_boolean: bool_t = True,
    convert_floating: bool_t = True,
) -> FrameOrSeries:
    """
    Convert columns to best possible dtypes using dtypes supporting ``pd.NA``.

    .. versionadded:: 1.0.0

    Parameters
    ----------
    infer_objects : bool, default True
        Whether object dtypes should be converted to the best possible types.
    convert_string : bool, default True
        Whether object dtypes should be converted to ``StringDtype()``.
    convert_integer : bool, default True
        Whether, if possible, conversion can be done to integer extension types.
    convert_boolean : bool, defaults True
        Whether object dtypes should be converted to ``BooleanDtypes()``.
    convert_floating : bool, defaults True
        Whether, if possible, conversion can be done to floating extension types.
        If `convert_integer` is also True, preference will be give to integer
        dtypes if the floats can be faithfully casted to integers.

        .. versionadded:: 1.2.0

    Returns
    -------
    Series or DataFrame
        Copy of input object with new dtype.

    See Also
    --------
    infer_objects : Infer dtypes of objects.
    to_datetime : Convert argument to datetime.
    to_timedelta : Convert argument to timedelta.
    to_numeric : Convert argument to a numeric type.

    Notes
    -----
    By default, ``convert_dtypes`` will attempt to convert a Series (or each
    Series in a DataFrame) to dtypes that support ``pd.NA``. By using the options
    ``convert_string``, ``convert_integer``, ``convert_boolean`` and
    ``convert_boolean``, it is possible to turn off individual conversions
    to ``StringDtype``, the integer extension types, ``BooleanDtype``
    or floating extension types, respectively.

    For object-dtyped columns, if ``infer_objects`` is ``True``, use the inference
    rules as during normal Series/DataFrame construction.  Then, if possible,
    convert to ``StringDtype``, ``BooleanDtype`` or an appropriate integer
    or floating extension type, otherwise leave as ``object``.

    If the dtype is integer, convert to an appropriate integer extension type.

    If the dtype is numeric, and consists of all integers, convert to an
    appropriate integer extension type. Otherwise, convert to an
    appropriate floating extension type.

    .. versionchanged:: 1.2
        Starting with pandas 1.2, this method also converts float columns
        to the nullable floating extension type.

    In the future, as new dtypes are added that support ``pd.NA``, the results
    of this method will change to support those new dtypes.

    Examples
    --------
    >>> df = pd.DataFrame(
    ...     {
    ...         "a": pd.Series([1, 2, 3], dtype=np.dtype("int32")),
    ...         "b": pd.Series(["x", "y", "z"], dtype=np.dtype("O")),
    ...         "c": pd.Series([True, False, np.nan], dtype=np.dtype("O")),
    ...         "d": pd.Series(["h", "i", np.nan], dtype=np.dtype("O")),
    ...         "e": pd.Series([10, np.nan, 20], dtype=np.dtype("float")),
    ...         "f": pd.Series([np.nan, 100.5, 200], dtype=np.dtype("float")),
    ...     }
    ... )

    Start with a DataFrame with default dtypes.

    >>> df
       a  b      c    d     e      f
    0  1  x   True    h  10.0    NaN
    1  2  y  False    i   NaN  100.5
    2  3  z    NaN  NaN  20.0  200.0

    >>> df.dtypes
    a      int32
    b     object
    c     object
    d     object
    e    float64
    f    float64
    dtype: object

    Convert the DataFrame to use best possible dtypes.

    >>> dfn = custom_convert_dtypes(df)
    >>> dfn
       a  b      c     d     e      f
    0  1  x   True     h    10   <NA>
    1  2  y  False     i  <NA>  100.5
    2  3  z   <NA>  <NA>    20  200.0

    >>> dfn.dtypes
    a      Int32
    b     string
    c    boolean
    d     string
    e      Int64
    f    Float64
    dtype: object

    Start with a Series of strings and missing data represented by ``np.nan``.

    >>> s = pd.Series(["a", "b", np.nan])
    >>> s
    0      a
    1      b
    2    NaN
    dtype: object

    Obtain a Series with dtype ``StringDtype``.

    >>> custom_convert_dtypes(s)
    0       a
    1       b
    2    <NA>
    dtype: string
    """
    if obj.ndim == 1:
        return obj._convert_dtypes(
            infer_objects,
            convert_string,
            convert_integer,
            convert_boolean,
            convert_floating,
        )
    else:
        results = [
            _convert_dtypes(
                col,
                infer_objects,
                convert_string,
                convert_integer,
                convert_boolean,
                convert_floating,
            )
            for col_name, col in obj.items()
        ]
        if len(results) > 0:
            return concat(results, axis=1, copy=False)
        else:
            return obj.copy()


def _convert_dtypes(
    df,
    infer_objects: bool = True,
    convert_string: bool = True,
    convert_integer: bool = True,
    convert_boolean: bool = True,
    convert_floating: bool = True,
) -> Series:
    input_series = df
    if infer_objects:
        input_series = input_series.infer_objects()
        if is_object_dtype(input_series):
            input_series = input_series.copy()

    if convert_string or convert_integer or convert_boolean or convert_floating:
        inferred_dtype = convert_dtypes(
            input_series._values,
            convert_string,
            convert_integer,
            convert_boolean,
            convert_floating,
        )
        type_ = _NUMBER_TYPE_MAP.get(inferred_dtype)
        if type_:
            elements_count = input_series.value_counts().to_dict()
            not_valid_elements = set()
            for element in elements_count:
                if element not in {pd.NA, np.nan, ""}:
                    if isinstance(element, int) or isinstance(element, float):
                        continue
                    not_valid_elements.add(element)
            if (
                input_series.size - elements_count.get("", 0) < input_series.size
                and not not_valid_elements
            ):
                result = input_series.copy()
                result = result.replace(r"^\s*$", pd.NA, regex=True)
                result = result.astype(type_)
            elif not_valid_elements:
                result = input_series.astype(input_series.dtype)
        else:
            result = input_series.astype(inferred_dtype)
    else:
        result = input_series.copy()
    return result


def convert_dtypes(
    input_array: ArrayLike,
    convert_string: bool = True,
    convert_integer: bool = True,
    convert_boolean: bool = True,
    convert_floating: bool = True,
) -> DtypeObj:
    """
    Convert objects to best possible type, and optionally,
    to types supporting ``pd.NA``.

    Parameters
    ----------
    input_array : ExtensionArray or np.ndarray
    convert_string : bool, default True
        Whether object dtypes should be converted to ``StringDtype()``.
    convert_integer : bool, default True
        Whether, if possible, conversion can be done to integer extension types.
    convert_boolean : bool, defaults True
        Whether object dtypes should be converted to ``BooleanDtypes()``.
    convert_floating : bool, defaults True
        Whether, if possible, conversion can be done to floating extension types.
        If `convert_integer` is also True, preference will be give to integer
        dtypes if the floats can be faithfully casted to integers.

    Returns
    -------
    np.dtype, or ExtensionDtype
    """
    # inferred_dtype: str | DtypeObj

    if (
        convert_string or convert_integer or convert_boolean or convert_floating
    ) and isinstance(input_array, np.ndarray):

        if is_object_dtype(input_array.dtype):
            inferred_dtype = lib.infer_dtype(input_array)
        else:
            inferred_dtype = input_array.dtype

        if is_string_dtype(inferred_dtype):
            if not convert_string or inferred_dtype == "bytes":
                return input_array.dtype
            else:
                return pandas_dtype("string")

        if convert_integer:
            target_int_dtype = pandas_dtype("Int64")

            if is_integer_dtype(input_array.dtype):
                from pandas.core.arrays.integer import INT_STR_TO_DTYPE

                inferred_dtype = INT_STR_TO_DTYPE.get(
                    input_array.dtype.name, target_int_dtype
                )
            elif is_numeric_dtype(input_array.dtype):
                # TODO: de-dup with maybe_cast_to_integer_array?
                arr = input_array[notna(input_array)]
                # Check np.int64 some OS return int == int32 numpy
                if (arr.astype(int) == arr).all() or (
                    arr.astype(np.int64) == arr
                ).all():
                    inferred_dtype = target_int_dtype
                else:
                    inferred_dtype = input_array.dtype

        if convert_floating:
            if not is_integer_dtype(input_array.dtype) and is_numeric_dtype(
                input_array.dtype
            ):
                from pandas.core.arrays.floating import FLOAT_STR_TO_DTYPE

                inferred_float_dtype: DtypeObj = FLOAT_STR_TO_DTYPE.get(
                    input_array.dtype.name, pandas_dtype("Float64")
                )
                # if we could also convert to integer, check if all floats
                # are actually integers
                if convert_integer:
                    # TODO: de-dup with maybe_cast_to_integer_array?
                    arr = input_array[notna(input_array)]
                    # Check np.int64 some OS return int == int32 numpy
                    if (arr.astype(int) == arr).all() or (
                        arr.astype(np.int64) == arr
                    ).all():
                        inferred_dtype = pandas_dtype("Int64")
                    else:
                        inferred_dtype = inferred_float_dtype
                else:
                    inferred_dtype = inferred_float_dtype

        if convert_boolean:
            if is_bool_dtype(input_array.dtype):
                inferred_dtype = pandas_dtype("boolean")
            elif isinstance(inferred_dtype, str) and inferred_dtype == "boolean":
                inferred_dtype = pandas_dtype("boolean")

        if _NUMBER_TYPE_MAP.get(inferred_dtype):
            return inferred_dtype
        if isinstance(inferred_dtype, str):
            # If we couldn't do anything else, then we retain the dtype
            inferred_dtype = input_array.dtype

    else:
        return input_array.dtype

    # error: Incompatible return value type (got "Union[str, Union[dtype[Any],
    # ExtensionDtype]]", expected "Union[dtype[Any], ExtensionDtype]")
    return inferred_dtype  # type: ignore[return-value]
