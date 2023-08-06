"""_530.py

SpiralBevelRateableMesh
"""


from mastapy._internal import constructor
from mastapy.gears.rating.agma_gleason_conical import _534
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_RATEABLE_MESH = python_net_import('SMT.MastaAPI.Gears.Rating.Bevel.Standards', 'SpiralBevelRateableMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelRateableMesh',)


class SpiralBevelRateableMesh(_534.AGMAGleasonConicalRateableMesh):
    """SpiralBevelRateableMesh

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_RATEABLE_MESH

    def __init__(self, instance_to_wrap: 'SpiralBevelRateableMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def safety_factor_scoring(self) -> 'float':
        """float: 'SafetyFactorScoring' is the original name of this property."""

        temp = self.wrapped.SafetyFactorScoring

        if temp is None:
            return None

        return temp

    @safety_factor_scoring.setter
    def safety_factor_scoring(self, value: 'float'):
        self.wrapped.SafetyFactorScoring = float(value) if value else 0.0
