"""_932.py

SpiralBevelGearDesign
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.bevel import _1134
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.SpiralBevel', 'SpiralBevelGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearDesign',)


class SpiralBevelGearDesign(_1134.BevelGearDesign):
    """SpiralBevelGearDesign

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'SpiralBevelGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mean_spiral_angle(self) -> 'float':
        """float: 'MeanSpiralAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanSpiralAngle

        if temp is None:
            return None

        return temp

    @property
    def recommended_maximum_face_width(self) -> 'float':
        """float: 'RecommendedMaximumFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RecommendedMaximumFaceWidth

        if temp is None:
            return None

        return temp
