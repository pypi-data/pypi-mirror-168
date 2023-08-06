"""_6164.py

ConicalGearCompoundDynamicAnalysis
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6034
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6190
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ConicalGearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearCompoundDynamicAnalysis',)


class ConicalGearCompoundDynamicAnalysis(_6190.GearCompoundDynamicAnalysis):
    """ConicalGearCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConicalGearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planetaries(self) -> 'List[ConicalGearCompoundDynamicAnalysis]':
        """List[ConicalGearCompoundDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6034.ConicalGearDynamicAnalysis]':
        """List[ConicalGearDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_6034.ConicalGearDynamicAnalysis]':
        """List[ConicalGearDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
