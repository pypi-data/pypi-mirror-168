"""_1557.py

CustomRow
"""


from mastapy._internal import constructor
from mastapy.utility.report import _1552
from mastapy._internal.python_net import python_net_import

_CUSTOM_ROW = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomRow')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomRow',)


class CustomRow(_1552.CustomReportPropertyItem):
    """CustomRow

    This is a mastapy class.
    """

    TYPE = _CUSTOM_ROW

    def __init__(self, instance_to_wrap: 'CustomRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def calculate_sum_of_values(self) -> 'bool':
        """bool: 'CalculateSumOfValues' is the original name of this property."""

        temp = self.wrapped.CalculateSumOfValues

        if temp is None:
            return None

        return temp

    @calculate_sum_of_values.setter
    def calculate_sum_of_values(self, value: 'bool'):
        self.wrapped.CalculateSumOfValues = bool(value) if value else False

    @property
    def count_values(self) -> 'bool':
        """bool: 'CountValues' is the original name of this property."""

        temp = self.wrapped.CountValues

        if temp is None:
            return None

        return temp

    @count_values.setter
    def count_values(self, value: 'bool'):
        self.wrapped.CountValues = bool(value) if value else False

    @property
    def is_minor_value(self) -> 'bool':
        """bool: 'IsMinorValue' is the original name of this property."""

        temp = self.wrapped.IsMinorValue

        if temp is None:
            return None

        return temp

    @is_minor_value.setter
    def is_minor_value(self, value: 'bool'):
        self.wrapped.IsMinorValue = bool(value) if value else False

    @property
    def overridden_property_name(self) -> 'str':
        """str: 'OverriddenPropertyName' is the original name of this property."""

        temp = self.wrapped.OverriddenPropertyName

        if temp is None:
            return None

        return temp

    @overridden_property_name.setter
    def overridden_property_name(self, value: 'str'):
        self.wrapped.OverriddenPropertyName = str(value) if value else ''

    @property
    def override_property_name(self) -> 'bool':
        """bool: 'OverridePropertyName' is the original name of this property."""

        temp = self.wrapped.OverridePropertyName

        if temp is None:
            return None

        return temp

    @override_property_name.setter
    def override_property_name(self, value: 'bool'):
        self.wrapped.OverridePropertyName = bool(value) if value else False

    @property
    def show_maximum_of_absolute_values(self) -> 'bool':
        """bool: 'ShowMaximumOfAbsoluteValues' is the original name of this property."""

        temp = self.wrapped.ShowMaximumOfAbsoluteValues

        if temp is None:
            return None

        return temp

    @show_maximum_of_absolute_values.setter
    def show_maximum_of_absolute_values(self, value: 'bool'):
        self.wrapped.ShowMaximumOfAbsoluteValues = bool(value) if value else False

    @property
    def show_maximum_of_values(self) -> 'bool':
        """bool: 'ShowMaximumOfValues' is the original name of this property."""

        temp = self.wrapped.ShowMaximumOfValues

        if temp is None:
            return None

        return temp

    @show_maximum_of_values.setter
    def show_maximum_of_values(self, value: 'bool'):
        self.wrapped.ShowMaximumOfValues = bool(value) if value else False

    @property
    def show_minimum_of_values(self) -> 'bool':
        """bool: 'ShowMinimumOfValues' is the original name of this property."""

        temp = self.wrapped.ShowMinimumOfValues

        if temp is None:
            return None

        return temp

    @show_minimum_of_values.setter
    def show_minimum_of_values(self, value: 'bool'):
        self.wrapped.ShowMinimumOfValues = bool(value) if value else False
