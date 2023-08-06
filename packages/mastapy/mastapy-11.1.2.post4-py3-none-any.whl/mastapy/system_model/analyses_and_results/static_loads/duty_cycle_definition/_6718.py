"""_6718.py

DesignStateOptions
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.analyses_and_results.load_case_groups import _5397
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model import _1963
from mastapy.utility_gui import _1622
from mastapy._internal.python_net import python_net_import

_DESIGN_STATE_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'DesignStateOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignStateOptions',)


class DesignStateOptions(_1622.ColumnInputOptions):
    """DesignStateOptions

    This is a mastapy class.
    """

    TYPE = _DESIGN_STATE_OPTIONS

    def __init__(self, instance_to_wrap: 'DesignStateOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def create_new_design_state(self) -> 'bool':
        """bool: 'CreateNewDesignState' is the original name of this property."""

        temp = self.wrapped.CreateNewDesignState

        if temp is None:
            return None

        return temp

    @create_new_design_state.setter
    def create_new_design_state(self, value: 'bool'):
        self.wrapped.CreateNewDesignState = bool(value) if value else False

    @property
    def design_state(self) -> 'list_with_selected_item.ListWithSelectedItem_DesignState':
        """list_with_selected_item.ListWithSelectedItem_DesignState: 'DesignState' is the original name of this property."""

        temp = self.wrapped.DesignState

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_DesignState)(temp) if temp is not None else None

    @design_state.setter
    def design_state(self, value: 'list_with_selected_item.ListWithSelectedItem_DesignState.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_DesignState.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_DesignState.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.DesignState = value

    @property
    def design_state_destinations(self) -> 'List[_1963.DutyCycleImporterDesignEntityMatch[_5397.DesignState]]':
        """List[DutyCycleImporterDesignEntityMatch[DesignState]]: 'DesignStateDestinations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DesignStateDestinations

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
