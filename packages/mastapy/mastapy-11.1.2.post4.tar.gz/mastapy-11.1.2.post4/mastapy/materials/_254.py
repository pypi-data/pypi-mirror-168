"""_254.py

SafetyFactorItem
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SAFETY_FACTOR_ITEM = python_net_import('SMT.MastaAPI.Materials', 'SafetyFactorItem')


__docformat__ = 'restructuredtext en'
__all__ = ('SafetyFactorItem',)


class SafetyFactorItem(_0.APIBase):
    """SafetyFactorItem

    This is a mastapy class.
    """

    TYPE = _SAFETY_FACTOR_ITEM

    def __init__(self, instance_to_wrap: 'SafetyFactorItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def damage(self) -> 'float':
        """float: 'Damage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Damage

        if temp is None:
            return None

        return temp

    @property
    def description(self) -> 'str':
        """str: 'Description' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Description

        if temp is None:
            return None

        return temp

    @property
    def minimum_required_safety_factor(self) -> 'float':
        """float: 'MinimumRequiredSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumRequiredSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def reliability(self) -> 'float':
        """float: 'Reliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Reliability

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
    def time_until_failure(self) -> 'float':
        """float: 'TimeUntilFailure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TimeUntilFailure

        if temp is None:
            return None

        return temp
