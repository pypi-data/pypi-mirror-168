"""_3681.py

CVTPulleyCompoundStabilityAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.stability_analyses import _3549
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3727
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'CVTPulleyCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundStabilityAnalysis',)


class CVTPulleyCompoundStabilityAnalysis(_3727.PulleyCompoundStabilityAnalysis):
    """CVTPulleyCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_PULLEY_COMPOUND_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_3549.CVTPulleyStabilityAnalysis]':
        """List[CVTPulleyStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3549.CVTPulleyStabilityAnalysis]':
        """List[CVTPulleyStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
