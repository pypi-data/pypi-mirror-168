"""_368.py

StraightBevelGearRating
"""


from mastapy.gears.gear_designs.straight_bevel import _924
from mastapy._internal import constructor
from mastapy.gears.rating.bevel import _521
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.StraightBevel', 'StraightBevelGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearRating',)


class StraightBevelGearRating(_521.BevelGearRating):
    """StraightBevelGearRating

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_GEAR_RATING

    def __init__(self, instance_to_wrap: 'StraightBevelGearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def straight_bevel_gear(self) -> '_924.StraightBevelGearDesign':
        """StraightBevelGearDesign: 'StraightBevelGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelGear

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
