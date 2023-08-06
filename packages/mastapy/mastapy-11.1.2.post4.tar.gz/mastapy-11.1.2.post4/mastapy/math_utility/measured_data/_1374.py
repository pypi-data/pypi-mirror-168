"""_1374.py

LookupTableBase
"""


from typing import Generic, TypeVar

from mastapy._internal.implicit import enum_with_selected_value
from mastapy.math_utility import _1317
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.utility import _1390
from mastapy._internal.python_net import python_net_import

_LOOKUP_TABLE_BASE = python_net_import('SMT.MastaAPI.MathUtility.MeasuredData', 'LookupTableBase')


__docformat__ = 'restructuredtext en'
__all__ = ('LookupTableBase',)


T = TypeVar('T', bound='LookupTableBase')


class LookupTableBase(_1390.IndependentReportablePropertiesBase['T'], Generic[T]):
    """LookupTableBase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _LOOKUP_TABLE_BASE

    def __init__(self, instance_to_wrap: 'LookupTableBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def extrapolation_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions':
        """enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions: 'ExtrapolationOption' is the original name of this property."""

        temp = self.wrapped.ExtrapolationOption

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @extrapolation_option.setter
    def extrapolation_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ExtrapolationOption = value
