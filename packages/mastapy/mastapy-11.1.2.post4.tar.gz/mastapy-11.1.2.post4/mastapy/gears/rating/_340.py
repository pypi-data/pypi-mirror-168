"""_340.py

SafetyFactorResults
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SAFETY_FACTOR_RESULTS = python_net_import('SMT.MastaAPI.Gears.Rating', 'SafetyFactorResults')


__docformat__ = 'restructuredtext en'
__all__ = ('SafetyFactorResults',)


class SafetyFactorResults(_0.APIBase):
    """SafetyFactorResults

    This is a mastapy class.
    """

    TYPE = _SAFETY_FACTOR_RESULTS

    def __init__(self, instance_to_wrap: 'SafetyFactorResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fatigue_bending_safety_factor(self) -> 'float':
        """float: 'FatigueBendingSafetyFactor' is the original name of this property."""

        temp = self.wrapped.FatigueBendingSafetyFactor

        if temp is None:
            return None

        return temp

    @fatigue_bending_safety_factor.setter
    def fatigue_bending_safety_factor(self, value: 'float'):
        self.wrapped.FatigueBendingSafetyFactor = float(value) if value else 0.0

    @property
    def fatigue_contact_safety_factor(self) -> 'float':
        """float: 'FatigueContactSafetyFactor' is the original name of this property."""

        temp = self.wrapped.FatigueContactSafetyFactor

        if temp is None:
            return None

        return temp

    @fatigue_contact_safety_factor.setter
    def fatigue_contact_safety_factor(self, value: 'float'):
        self.wrapped.FatigueContactSafetyFactor = float(value) if value else 0.0

    @property
    def fatigue_safety_factor(self) -> 'float':
        """float: 'FatigueSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def safety_factor(self) -> 'float':
        """float: 'SafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def static_bending_safety_factor(self) -> 'float':
        """float: 'StaticBendingSafetyFactor' is the original name of this property."""

        temp = self.wrapped.StaticBendingSafetyFactor

        if temp is None:
            return None

        return temp

    @static_bending_safety_factor.setter
    def static_bending_safety_factor(self, value: 'float'):
        self.wrapped.StaticBendingSafetyFactor = float(value) if value else 0.0

    @property
    def static_contact_safety_factor(self) -> 'float':
        """float: 'StaticContactSafetyFactor' is the original name of this property."""

        temp = self.wrapped.StaticContactSafetyFactor

        if temp is None:
            return None

        return temp

    @static_contact_safety_factor.setter
    def static_contact_safety_factor(self, value: 'float'):
        self.wrapped.StaticContactSafetyFactor = float(value) if value else 0.0

    @property
    def static_safety_factor(self) -> 'float':
        """float: 'StaticSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticSafetyFactor

        if temp is None:
            return None

        return temp
