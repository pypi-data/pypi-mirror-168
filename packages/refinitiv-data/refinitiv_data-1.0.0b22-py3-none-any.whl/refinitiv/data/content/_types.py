from typing import Optional, Callable, List, Union
from datetime import date, datetime, timedelta

OptStr = Optional[str]
Strings = List[str]
Dicts = List[dict]
OptStrings = Optional[Strings]
OptDicts = Optional[Dicts]

OptInt = Optional[int]
OptFloat = Optional[float]
OptList = Optional[list]
OptTuple = Optional[tuple]
OptDict = Optional[dict]
OptSet = Optional[set]
OptBool = Optional[bool]
OptCall = Optional[Callable]

ExtendedParams = OptDict
Universe = Union[str, List[str]]
OptFields = Optional[Universe]
OptDateTime = Optional[Union[str, date, datetime, timedelta]]
DateTime = Union[str, date, datetime, timedelta]
