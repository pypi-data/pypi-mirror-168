"""_5398.py

DutyCycle
"""


from typing import List

from mastapy.system_model.analyses_and_results.load_case_groups import _5401, _5394
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition import _6729
from mastapy.system_model.analyses_and_results.static_loads import _6528
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'DutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycle',)


class DutyCycle(_5394.AbstractStaticLoadCaseGroup):
    """DutyCycle

    This is a mastapy class.
    """

    TYPE = _DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'DutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_design_states(self) -> 'List[_5401.SubGroupInSingleDesignState]':
        """List[SubGroupInSingleDesignState]: 'DutyCycleDesignStates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DutyCycleDesignStates

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def time_series_importer(self) -> '_6729.TimeSeriesImporter':
        """TimeSeriesImporter: 'TimeSeriesImporter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TimeSeriesImporter

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def convert_to_condensed_parametric_study_tool_duty_cycle(self):
        """ 'ConvertToCondensedParametricStudyToolDutyCycle' is the original name of this method."""

        self.wrapped.ConvertToCondensedParametricStudyToolDutyCycle()

    def add_static_load(self, static_load: '_6528.StaticLoadCase'):
        """ 'AddStaticLoad' is the original name of this method.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
        """

        self.wrapped.AddStaticLoad(static_load.wrapped if static_load else None)

    def delete(self):
        """ 'Delete' is the original name of this method."""

        self.wrapped.Delete()

    def remove_design_state_sub_group(self, sub_group: '_5401.SubGroupInSingleDesignState'):
        """ 'RemoveDesignStateSubGroup' is the original name of this method.

        Args:
            sub_group (mastapy.system_model.analyses_and_results.load_case_groups.SubGroupInSingleDesignState)
        """

        self.wrapped.RemoveDesignStateSubGroup(sub_group.wrapped if sub_group else None)

    def remove_static_load(self, static_load: '_6528.StaticLoadCase'):
        """ 'RemoveStaticLoad' is the original name of this method.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
        """

        self.wrapped.RemoveStaticLoad(static_load.wrapped if static_load else None)
