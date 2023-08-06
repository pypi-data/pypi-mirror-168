from typing import Optional, Callable, TYPE_CHECKING

from ._stream_facade import Stream
from .._content_type import ContentType
from ..._core.session import Session
from ..._tools import create_repr
from ..._tools._common import universe_arg_parser, fields_arg_parser
from ...delivery._data._data_provider import DataProviderLayer, BaseResponse, Data

if TYPE_CHECKING:
    from .._types import OptStr, ExtendedParams, Universe, OptFields


class Definition(DataProviderLayer[BaseResponse[Data]]):
    """
    This class defines parameters for requesting events from pricing

    Parameters
    ----------
    universe : str or list of str
        The single/multiple instrument/s name (e.g. "EUR=" or ["EUR=", "CAD=", "UAH="]).
    fields : str or list of str, optional
        Specifies the specific fields to be delivered when messages arrive
    service : str, optional
        Name of the streaming service publishing the instruments
    closure : Callable, optional
        Specifies the parameter that will be merged with the request
    api: str, optional
        Specifies the data source. It can be updated/added using config file
    extended_params : dict, optional
        Other parameters can be provided if necessary

    Examples
    --------
    >>> from refinitiv.data.content import pricing
    >>> definition = pricing.Definition("EUR=")
    >>> response = definition.get_data()

    """

    def __init__(
        self,
        universe: "Universe",
        fields: "OptFields" = None,
        service: "OptStr" = None,
        closure: Optional[Callable] = None,
        api: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ) -> None:
        extended_params = extended_params or {}
        universe = extended_params.pop("universe", universe)
        universe = universe_arg_parser.get_list(universe)
        fields = extended_params.pop("fields", fields)
        fields = fields_arg_parser.get_unique(fields or [])
        super().__init__(
            data_type=ContentType.PRICING,
            universe=universe,
            fields=fields,
            closure=closure,
            extended_params=extended_params,
        )
        self._universe = universe
        self._fields = fields
        self._service = service
        self._api = api
        self._extended_params = extended_params

    def __repr__(self) -> str:
        return create_repr(
            self,
            content=f"{{name={self._universe}}}",
        )

    def get_stream(self, session: Session = None) -> Stream:
        """
        Summary line of this func create a pricing.Stream object for the defined data

        Parameters
        ----------
        session : Session, optional
            The Session defines the source where you want to retrieve your data

        Returns
        -------
        pricing.Stream

        Examples
        --------
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition("IBM")
        >>> stream = definition.get_stream()
        >>> stream.open()
        """
        return Stream(
            universe=self._universe,
            session=session,
            fields=self._fields,
            service=self._service,
            api=self._api,
            extended_params=self._extended_params,
        )
