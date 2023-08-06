from ..._ipa_content_provider import IPAContentProviderLayer
from ..._surfaces._eti_surface_request_item import EtiSurfaceRequestItem
from ...._content_type import ContentType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...._types import ExtendedParams


class Definition(IPAContentProviderLayer):
    def __init__(
        self,
        surface_layout,
        surface_parameters,
        underlying_definition,
        surface_tag,
        extended_params: "ExtendedParams" = None,
    ):
        request_item = EtiSurfaceRequestItem(
            surface_layout=surface_layout,
            surface_parameters=surface_parameters,
            underlying_definition=underlying_definition,
            surface_tag=surface_tag,
        )
        super().__init__(
            content_type=ContentType.SURFACES,
            universe=request_item,
            extended_params=extended_params,
        )
