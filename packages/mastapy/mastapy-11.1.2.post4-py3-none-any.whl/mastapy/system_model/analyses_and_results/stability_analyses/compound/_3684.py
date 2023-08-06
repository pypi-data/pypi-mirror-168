"""_3684.py

CycloidalDiscCompoundStabilityAnalysis
"""


from typing import List

from mastapy.system_model.part_model.cycloidal import _2318
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3554
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3640
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'CycloidalDiscCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCompoundStabilityAnalysis',)


class CycloidalDiscCompoundStabilityAnalysis(_3640.AbstractShaftCompoundStabilityAnalysis):
    """CycloidalDiscCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_COMPOUND_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'CycloidalDiscCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2318.CycloidalDisc':
        """CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3554.CycloidalDiscStabilityAnalysis]':
        """List[CycloidalDiscStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3554.CycloidalDiscStabilityAnalysis]':
        """List[CycloidalDiscStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
