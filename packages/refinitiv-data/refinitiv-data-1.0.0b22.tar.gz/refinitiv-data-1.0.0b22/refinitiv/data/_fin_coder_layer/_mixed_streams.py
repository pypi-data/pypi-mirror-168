from typing import Dict

from .._tools import cached_property
from ..content._content_type import ContentType
from ..content._universe_stream import _UniverseStream
from ..content._universe_streams import _UniverseStreams
from ..content.custom_instruments._custom_instruments_data_provider import (
    is_instrument_id,
    get_user_id,
)
from ..content.custom_instruments._stream_facade import uuid_from_symbol
from ..content.pricing._stream_facade import Stream as _Stream, PricingStream
from ..delivery._data._data_provider import DataProviderLayer
from ..delivery._data._endpoint_data import RequestMethod
from ..delivery._stream import StreamStateEvent


class MixedStreams(_UniverseStreams):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, content_type=ContentType.NONE)
        self._uuid = None

    def _get_symbol(self, universe):
        if is_instrument_id.match(universe):
            data_provider_layer = DataProviderLayer(
                data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
                universe=self.universe,
            )
            instrument_response = data_provider_layer.get_data(
                self._session, method=RequestMethod.GET
            )
            symbol = instrument_response.data.raw.get("symbol")
            if not self._uuid:
                self._uuid = uuid_from_symbol(symbol)
        else:
            if "." not in universe:
                if not self._uuid:
                    self._uuid = get_user_id(self._session)
                symbol = f"{universe}.{self._uuid}"
            else:
                symbol = universe
        return symbol

    def _get_pricing_stream(self, name):
        stream = _UniverseStream(
            content_type=ContentType.STREAMING_PRICING,
            session=self._session,
            name=name,
            fields=self.fields,
            service=self._service,
            on_refresh=self._on_stream_refresh,
            on_status=self._on_stream_status,
            on_update=self._on_stream_update,
            on_complete=self._on_stream_complete,
            on_error=self._on_stream_error,
            extended_params=self._extended_params,
            parent_id=self._id,
        )
        return stream

    def _get_custom_instruments_stream(self, name):
        stream = _UniverseStream(
            content_type=ContentType.STREAMING_CUSTOM_INSTRUMENTS,
            session=self._session,
            name=self._get_symbol(name),
            fields=self.fields,
            service=self._service,
            on_refresh=self._on_stream_refresh,
            on_status=self._on_stream_status,
            on_update=self._on_stream_update,
            on_complete=self._on_stream_complete,
            on_error=self._on_stream_error,
            extended_params=self._extended_params,
            parent_id=self._id,
        )
        return stream

    def _get_stream_by_name(self, name):
        if name.startswith("S)"):
            stream = self._get_custom_instruments_stream(name)
        else:
            stream = self._get_pricing_stream(name)
        return stream

    @cached_property
    def _stream_by_name(self) -> Dict[str, _UniverseStream]:
        retval = {}
        for name in self.universe:
            stream = self._get_stream_by_name(name)
            stream.on(StreamStateEvent.CLOSED, self._on_stream_close)
            retval[name] = stream
        return retval

    def add_items(self, *args):
        args = [
            self._get_symbol(name) if name.startswith("S)") else name for name in args
        ]
        super().add_items(*args)

    def remove_items(self, *args):
        args = [
            self._get_symbol(name) if name.startswith("S)") else name for name in args
        ]
        super().remove_items(*args)


class Stream(_Stream):
    @cached_property
    def _stream(self) -> MixedStreams:
        return MixedStreams(
            item_facade_class=PricingStream,
            universe=self._universe,
            session=self._session,
            fields=self._fields,
            service=self._service,
            extended_params=self._extended_params,
        )
