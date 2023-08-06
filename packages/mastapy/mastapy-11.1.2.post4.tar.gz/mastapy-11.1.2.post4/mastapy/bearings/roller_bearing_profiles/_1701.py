"""_1701.py

RollerBearingUserSpecifiedProfile
"""


from typing import List

from mastapy.bearings.roller_bearing_profiles import (
    _1691, _1693, _1703, _1700
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.python_net import python_net_import

_ROLLER_BEARING_USER_SPECIFIED_PROFILE = python_net_import('SMT.MastaAPI.Bearings.RollerBearingProfiles', 'RollerBearingUserSpecifiedProfile')


__docformat__ = 'restructuredtext en'
__all__ = ('RollerBearingUserSpecifiedProfile',)


class RollerBearingUserSpecifiedProfile(_1700.RollerBearingProfile):
    """RollerBearingUserSpecifiedProfile

    This is a mastapy class.
    """

    TYPE = _ROLLER_BEARING_USER_SPECIFIED_PROFILE

    def __init__(self, instance_to_wrap: 'RollerBearingUserSpecifiedProfile.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def data_to_use(self) -> '_1691.ProfileDataToUse':
        """ProfileDataToUse: 'DataToUse' is the original name of this property."""

        temp = self.wrapped.DataToUse

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1691.ProfileDataToUse)(value) if value is not None else None

    @data_to_use.setter
    def data_to_use(self, value: '_1691.ProfileDataToUse'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DataToUse = value

    @property
    def number_of_points(self) -> 'int':
        """int: 'NumberOfPoints' is the original name of this property."""

        temp = self.wrapped.NumberOfPoints

        if temp is None:
            return None

        return temp

    @number_of_points.setter
    def number_of_points(self, value: 'int'):
        self.wrapped.NumberOfPoints = int(value) if value else 0

    @property
    def profile_to_fit(self) -> '_1693.ProfileToFit':
        """ProfileToFit: 'ProfileToFit' is the original name of this property."""

        temp = self.wrapped.ProfileToFit

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1693.ProfileToFit)(value) if value is not None else None

    @profile_to_fit.setter
    def profile_to_fit(self, value: '_1693.ProfileToFit'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProfileToFit = value

    @property
    def points(self) -> 'List[_1703.UserSpecifiedProfilePoint]':
        """List[UserSpecifiedProfilePoint]: 'Points' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Points

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def set_to_full_range(self):
        """ 'SetToFullRange' is the original name of this method."""

        self.wrapped.SetToFullRange()
