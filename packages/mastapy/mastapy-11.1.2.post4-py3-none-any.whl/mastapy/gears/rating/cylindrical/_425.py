"""_425.py

CylindricalGearFlankDutyCycleRating
"""


from mastapy.gears.rating import _331
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_FLANK_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearFlankDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearFlankDutyCycleRating',)


class CylindricalGearFlankDutyCycleRating(_331.GearFlankRating):
    """CylindricalGearFlankDutyCycleRating

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_FLANK_DUTY_CYCLE_RATING

    def __init__(self, instance_to_wrap: 'CylindricalGearFlankDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
