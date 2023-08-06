"""_6174.py

CVTPulleyCompoundDynamicAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.dynamic_analyses import _6044
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6220
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'CVTPulleyCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundDynamicAnalysis',)


class CVTPulleyCompoundDynamicAnalysis(_6220.PulleyCompoundDynamicAnalysis):
    """CVTPulleyCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_PULLEY_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_6044.CVTPulleyDynamicAnalysis]':
        """List[CVTPulleyDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6044.CVTPulleyDynamicAnalysis]':
        """List[CVTPulleyDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
