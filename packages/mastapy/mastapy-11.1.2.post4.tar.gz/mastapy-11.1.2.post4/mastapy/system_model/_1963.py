"""_1963.py

DutyCycleImporterDesignEntityMatch
"""


from typing import Generic, TypeVar

from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_IMPORTER_DESIGN_ENTITY_MATCH = python_net_import('SMT.MastaAPI.SystemModel', 'DutyCycleImporterDesignEntityMatch')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycleImporterDesignEntityMatch',)


T = TypeVar('T')


class DutyCycleImporterDesignEntityMatch(_0.APIBase, Generic[T]):
    """DutyCycleImporterDesignEntityMatch

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _DUTY_CYCLE_IMPORTER_DESIGN_ENTITY_MATCH

    def __init__(self, instance_to_wrap: 'DutyCycleImporterDesignEntityMatch.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def destination(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'Destination' is the original name of this property."""

        temp = self.wrapped.Destination

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @destination.setter
    def destination(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.Destination = value

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp
