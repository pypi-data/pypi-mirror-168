from typing import TYPE_CHECKING

from ..._ipa_content_provider import IPAContentProviderLayer
from ..._surfaces._cap_surface_request_item import CapSurfaceRequestItem
from ...._content_type import ContentType

if TYPE_CHECKING:
    from ...._types import ExtendedParams


class Definition(IPAContentProviderLayer):
    def __init__(
        self,
        surface_layout,
        surface_parameters,
        underlying_definition,
        surface_tag,
        instrument_type=None,
        extended_params: "ExtendedParams" = None,
    ):
        request_item = CapSurfaceRequestItem(
            instrument_type=instrument_type,
            surface_layout=surface_layout,
            surface_params=surface_parameters,
            underlying_definition=underlying_definition,
            surface_tag=surface_tag,
        )
        super().__init__(
            content_type=ContentType.SURFACES,
            universe=request_item,
            extended_params=extended_params,
        )
