"""_4278.py

ShaftCompoundParametricStudyTool
"""


from typing import List

from mastapy.system_model.part_model.shaft_model import _2232
from mastapy._internal import constructor, conversion
from mastapy.shafts import _19
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4150
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4184
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ShaftCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundParametricStudyTool',)


class ShaftCompoundParametricStudyTool(_4184.AbstractShaftCompoundParametricStudyTool):
    """ShaftCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _SHAFT_COMPOUND_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'ShaftCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2232.Shaft':
        """Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaft_duty_cycle_results(self) -> '_19.ShaftDamageResults':
        """ShaftDamageResults: 'ShaftDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftDutyCycleResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4150.ShaftParametricStudyTool]':
        """List[ShaftParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundParametricStudyTool]':
        """List[ShaftCompoundParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4150.ShaftParametricStudyTool]':
        """List[ShaftParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
