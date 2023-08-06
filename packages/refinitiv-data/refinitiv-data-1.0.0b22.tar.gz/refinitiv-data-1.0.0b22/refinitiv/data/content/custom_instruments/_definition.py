from typing import TYPE_CHECKING

from ._stream_facade import Stream, _init_universe
from ..._tools import universe_arg_parser

if TYPE_CHECKING:
    from .._types import OptStr, ExtendedParams, Universe


class Definition:
    """
    Allows to create custom instrument, symbol and formula fields are mandatory, others are optional

    Parameters
    -----------
    universe : str
        The Id or Symbol of custom instrument to operate on. Use only for get_instrument().
    api: str, optional
        Specifies the data source. It can be updated/added using config file
    extended_params : dict, optional
        If necessary other parameters

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments import Definition
    >>> definition = Definition(universe="MyNewInstrument")
    >>> stream = definition.get_stream()
    """

    def __init__(
        self,
        universe: "Universe",
        api: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ):
        extended_params = extended_params or {}
        universe = extended_params.pop("universe", universe)
        self._universe = universe_arg_parser.get_list(universe)
        self._api = api
        self._extended_params = extended_params

    def get_stream(self, session=None) -> Stream:
        universe = _init_universe(self._universe, session)
        stream = Stream(
            universe=universe,
            session=session,
            api=self._api,
            extended_params=self._extended_params,
        )
        return stream
