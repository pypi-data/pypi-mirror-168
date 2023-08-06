"""_931.py

StraightBevelDiffMeshedGearDesign
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.bevel import _1137
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_MESHED_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.StraightBevelDiff', 'StraightBevelDiffMeshedGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffMeshedGearDesign',)


class StraightBevelDiffMeshedGearDesign(_1137.BevelMeshedGearDesign):
    """StraightBevelDiffMeshedGearDesign

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_DIFF_MESHED_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'StraightBevelDiffMeshedGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def geometry_factor_j(self) -> 'float':
        """float: 'GeometryFactorJ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactorJ

        if temp is None:
            return None

        return temp

    @property
    def mean_topland(self) -> 'float':
        """float: 'MeanTopland' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanTopland

        if temp is None:
            return None

        return temp

    @property
    def strength_factor(self) -> 'float':
        """float: 'StrengthFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StrengthFactor

        if temp is None:
            return None

        return temp
