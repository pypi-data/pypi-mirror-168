"""_1082.py

ProfileReliefWithDeviation
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _987
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1084
from mastapy._internal.python_net import python_net_import

_PROFILE_RELIEF_WITH_DEVIATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'ProfileReliefWithDeviation')


__docformat__ = 'restructuredtext en'
__all__ = ('ProfileReliefWithDeviation',)


class ProfileReliefWithDeviation(_1084.ReliefWithDeviation):
    """ProfileReliefWithDeviation

    This is a mastapy class.
    """

    TYPE = _PROFILE_RELIEF_WITH_DEVIATION

    def __init__(self, instance_to_wrap: 'ProfileReliefWithDeviation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def profile_relief(self) -> 'float':
        """float: 'ProfileRelief' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileRelief

        if temp is None:
            return None

        return temp

    @property
    def roll_distance(self) -> 'float':
        """float: 'RollDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollDistance

        if temp is None:
            return None

        return temp

    @property
    def position_on_profile(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'PositionOnProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PositionOnProfile

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
