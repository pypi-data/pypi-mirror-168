"""_907.py

DesignConstraint
"""


from mastapy.utility import _1392
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.math_utility import _1295
from mastapy.math_utility.measured_ranges import _1372
from mastapy._internal.cast_exception import CastException
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.utility.model_validation import _1571
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DESIGN_CONSTRAINT = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'DesignConstraint')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignConstraint',)


class DesignConstraint(_0.APIBase):
    """DesignConstraint

    This is a mastapy class.
    """

    TYPE = _DESIGN_CONSTRAINT

    def __init__(self, instance_to_wrap: 'DesignConstraint.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def integer_range(self) -> '_1392.IntegerRange':
        """IntegerRange: 'IntegerRange' is the original name of this property."""

        temp = self.wrapped.IntegerRange

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @integer_range.setter
    def integer_range(self, value: '_1392.IntegerRange'):
        value = value.wrapped if value else None
        self.wrapped.IntegerRange = value

    @property
    def property_(self) -> 'str':
        """str: 'Property' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Property

        if temp is None:
            return None

        return temp

    @property
    def range(self) -> '_1295.Range':
        """Range: 'Range' is the original name of this property."""

        temp = self.wrapped.Range

        if temp is None:
            return None

        if _1295.Range.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast range to Range. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @range.setter
    def range(self, value: '_1295.Range'):
        value = value.wrapped if value else None
        self.wrapped.Range = value

    @property
    def severity(self) -> 'enum_with_selected_value.EnumWithSelectedValue_Severity':
        """enum_with_selected_value.EnumWithSelectedValue_Severity: 'Severity' is the original name of this property."""

        temp = self.wrapped.Severity

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_Severity.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @severity.setter
    def severity(self, value: 'enum_with_selected_value.EnumWithSelectedValue_Severity.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_Severity.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.Severity = value

    @property
    def type_(self) -> 'str':
        """str: 'Type' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Type

        if temp is None:
            return None

        return temp

    @property
    def unit(self) -> 'str':
        """str: 'Unit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Unit

        if temp is None:
            return None

        return temp
