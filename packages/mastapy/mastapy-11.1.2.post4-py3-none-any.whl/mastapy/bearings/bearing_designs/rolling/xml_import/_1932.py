"""_1932.py

AbstractXmlVariableAssignment
"""


from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_XML_VARIABLE_ASSIGNMENT = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling.XmlImport', 'AbstractXmlVariableAssignment')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractXmlVariableAssignment',)


class AbstractXmlVariableAssignment(_0.APIBase):
    """AbstractXmlVariableAssignment

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_XML_VARIABLE_ASSIGNMENT

    def __init__(self, instance_to_wrap: 'AbstractXmlVariableAssignment.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def definitions(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'Definitions' is the original name of this property."""

        temp = self.wrapped.Definitions

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @definitions.setter
    def definitions(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.Definitions = value

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
    def variable_name(self) -> 'str':
        """str: 'VariableName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VariableName

        if temp is None:
            return None

        return temp
