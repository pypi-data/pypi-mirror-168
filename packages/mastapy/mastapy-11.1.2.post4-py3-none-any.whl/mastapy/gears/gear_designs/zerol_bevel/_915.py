"""_915.py

ZerolBevelGearDesign
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.bevel import _1134
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.ZerolBevel', 'ZerolBevelGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearDesign',)


class ZerolBevelGearDesign(_1134.BevelGearDesign):
    """ZerolBevelGearDesign

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'ZerolBevelGearDesign.TYPE'):
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
