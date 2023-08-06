from typing import Any, Callable, List, Optional, TYPE_CHECKING, Union

from ._custom_instruments_data_provider import (
    is_instrument_id,
    get_valid_symbol,
    get_valid_symbol_request,
)
from .._content_type import ContentType
from .._types import OptStr
from .._universe_streams import UniverseStreamFacade, _UniverseStreams
from ..._tools import (
    PRICING_DATETIME_PATTERN,
    cached_property,
    create_repr,
    make_callback,
)
from ..._tools._dataframe import convert_df_columns_to_datetime_use_re_compile
from ...delivery._data._data_provider import DataProviderLayer
from ...delivery._data._endpoint_data import RequestMethod
from ...delivery._stream.base_stream import StreamOpenWithUpdatesMixin

if TYPE_CHECKING:
    import pandas
    from ... import OpenState
    from ..._core.session import Session


def uuid_from_symbol(symbol: str) -> str:
    return symbol.rsplit(".", 1)[-1]


def _init_universe(universe, session):
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        universe=universe,
    )

    uuid = None
    result = []
    for item in universe:
        # a20140be-3648-4892-9d1b-ce78ee8617fd
        if is_instrument_id.match(item):
            instrument_response = data_provider_layer.get_data(
                session, method=RequestMethod.GET
            )
            # S)MyNewInstrument5.GE-1525-0
            symbol = instrument_response.data.raw.get("symbol")

        else:
            # S)MyNewInstrument5
            if "." not in item and not uuid:
                # S)MyNewInstrument5.GE-1525-0
                symbol = get_valid_symbol_request(item, session)
                # GE-1525-0
                uuid = uuid_from_symbol(symbol)

            else:
                symbol = get_valid_symbol(item, uuid)

        result.append(symbol)

    return result


class CustomInstrumentsStream(UniverseStreamFacade):
    pass


class Stream(StreamOpenWithUpdatesMixin):
    def __init__(
        self,
        session: "Session" = None,
        universe: Union[str, List[str]] = None,
        fields: Optional[list] = None,
        service: OptStr = None,
        api: OptStr = None,
        extended_params: Optional[dict] = None,
    ) -> None:
        self._session = session
        self._universe = universe or []
        self._fields = fields
        self._service = service
        self._api = api
        self._extended_params = extended_params

    @cached_property
    def _stream(self) -> _UniverseStreams:
        if self._api:
            content_type = ContentType.STREAMING_CUSTOM
        else:
            content_type = ContentType.STREAMING_CUSTOM_INSTRUMENTS

        return _UniverseStreams(
            content_type=content_type,
            item_facade_class=CustomInstrumentsStream,
            universe=self._universe,
            session=self._session,
            fields=self._fields,
            service=self._service,
            api=self._api,
            extended_params=self._extended_params,
        )

    def open(self, with_updates: bool = True) -> "OpenState":
        self._stream.open(with_updates=with_updates)
        return self.open_state

    def close(self) -> "OpenState":
        self._stream.close()
        return self.open_state

    def _get_fields(self, universe: str, fields: Optional[list] = None) -> dict:
        _fields = {
            universe: {
                key: value
                for key, value in self._stream[universe].items()
                if fields is None or key in fields
            }
        }
        return _fields

    def get_snapshot(
        self,
        universe: Union[str, List[str], None] = None,
        fields: Optional[List[str]] = None,
        convert: bool = True,
    ) -> "pandas.DataFrame":
        df = self._stream.get_snapshot(
            universe=universe, fields=fields, convert=convert
        )
        convert_df_columns_to_datetime_use_re_compile(df, PRICING_DATETIME_PATTERN)
        return df

    def on_refresh(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        self._stream.on_refresh(make_callback(func))
        return self

    def on_update(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        self._stream.on_update(make_callback(func))
        return self

    def on_status(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        self._stream.on_status(make_callback(func))
        return self

    def on_complete(self, func: Callable[["Stream"], Any]) -> "Stream":
        self._stream.on_complete(func)
        return self

    def on_error(self, func: Callable) -> "Stream":
        self._stream.on_error(make_callback(func))
        return self

    def add_items(self, *args):
        args = _init_universe(args, self._session)
        self._stream.add_items(*args)

    def remove_items(self, *args):
        args = _init_universe(args, self._session)
        self._stream.remove_items(*args)

    def __iter__(self):
        return self._stream.__iter__()

    def __getitem__(self, item) -> "UniverseStreamFacade":
        return self._stream.__getitem__(item)

    def __len__(self) -> int:
        return self._stream.__len__()

    def __repr__(self):
        return create_repr(
            self,
            class_name=self.__class__.__name__,
            content=f"{{name='{self._universe}'}}",
        )
