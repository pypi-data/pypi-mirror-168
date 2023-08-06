"""_580.py

CylindricalGearSpecifiedProfile
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SPECIFIED_PROFILE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalGearSpecifiedProfile')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSpecifiedProfile',)


class CylindricalGearSpecifiedProfile(_0.APIBase):
    """CylindricalGearSpecifiedProfile

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_SPECIFIED_PROFILE

    def __init__(self, instance_to_wrap: 'CylindricalGearSpecifiedProfile.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def offset_at_minimum_roll_distance(self) -> 'float':
        """float: 'OffsetAtMinimumRollDistance' is the original name of this property."""

        temp = self.wrapped.OffsetAtMinimumRollDistance

        if temp is None:
            return None

        return temp

    @offset_at_minimum_roll_distance.setter
    def offset_at_minimum_roll_distance(self, value: 'float'):
        self.wrapped.OffsetAtMinimumRollDistance = float(value) if value else 0.0
