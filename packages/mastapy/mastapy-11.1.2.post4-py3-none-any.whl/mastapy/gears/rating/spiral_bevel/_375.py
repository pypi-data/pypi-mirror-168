"""_375.py

SpiralBevelGearRating
"""


from mastapy.gears.gear_designs.spiral_bevel import _932
from mastapy._internal import constructor
from mastapy.gears.rating.bevel import _521
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.SpiralBevel', 'SpiralBevelGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearRating',)


class SpiralBevelGearRating(_521.BevelGearRating):
    """SpiralBevelGearRating

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_RATING

    def __init__(self, instance_to_wrap: 'SpiralBevelGearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def spiral_bevel_gear(self) -> '_932.SpiralBevelGearDesign':
        """SpiralBevelGearDesign: 'SpiralBevelGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelGear

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
