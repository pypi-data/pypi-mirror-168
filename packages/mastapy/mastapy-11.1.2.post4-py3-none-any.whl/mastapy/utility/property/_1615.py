"""_1615.py

DutyCyclePropertySummaryPercentage
"""


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy.utility.property import _1613
from mastapy.utility.units_and_measurements.measurements import _1477
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_PROPERTY_SUMMARY_PERCENTAGE = python_net_import('SMT.MastaAPI.Utility.Property', 'DutyCyclePropertySummaryPercentage')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCyclePropertySummaryPercentage',)


T = TypeVar('T')


class DutyCyclePropertySummaryPercentage(_1613.DutyCyclePropertySummary['_1477.Percentage', 'T'], Generic[T]):
    """DutyCyclePropertySummaryPercentage

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _DUTY_CYCLE_PROPERTY_SUMMARY_PERCENTAGE

    def __init__(self, instance_to_wrap: 'DutyCyclePropertySummaryPercentage.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def average_value(self) -> 'float':
        """float: 'AverageValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageValue

        if temp is None:
            return None

        return temp

    @property
    def maximum_value(self) -> 'float':
        """float: 'MaximumValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumValue

        if temp is None:
            return None

        return temp

    @property
    def minimum_value(self) -> 'float':
        """float: 'MinimumValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumValue

        if temp is None:
            return None

        return temp
