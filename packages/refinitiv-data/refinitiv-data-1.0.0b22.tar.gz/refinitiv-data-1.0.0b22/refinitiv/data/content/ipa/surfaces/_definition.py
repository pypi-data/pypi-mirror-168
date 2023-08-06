from numpy import iterable

from .._ipa_content_provider import IPAContentProviderLayer
from ..._content_type import ContentType


class Definitions(IPAContentProviderLayer):
    def __init__(
        self,
        universe,
    ):
        if not iterable(universe):
            universe = [universe]

        super().__init__(
            content_type=ContentType.SURFACES,
            universe=universe,
            __plural__=True,
        )
