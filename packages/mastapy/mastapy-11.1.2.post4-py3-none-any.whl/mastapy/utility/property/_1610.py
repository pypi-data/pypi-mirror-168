"""_1610.py

EnumWithSelectedValue
"""


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import
from mastapy import _7279

_ARRAY = python_net_import('System', 'Array')
_ENUM_WITH_SELECTED_VALUE = python_net_import('SMT.MastaAPI.Utility.Property', 'EnumWithSelectedValue')


__docformat__ = 'restructuredtext en'
__all__ = ('EnumWithSelectedValue',)


TAPIEnum = TypeVar('TAPIEnum')


class EnumWithSelectedValue(_7279.MarshalByRefObjectPermanent, Generic[TAPIEnum]):
    """EnumWithSelectedValue

    This is a mastapy class.

    Generic Types:
        TAPIEnum
    """

    TYPE = _ENUM_WITH_SELECTED_VALUE

    def __init__(self, instance_to_wrap: 'EnumWithSelectedValue.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def selected_value(self) -> 'TAPIEnum':
        """TAPIEnum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedValue

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def available_values(self) -> 'List[TAPIEnum]':
        """List[TAPIEnum]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AvailableValues

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
