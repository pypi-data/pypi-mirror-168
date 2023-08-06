"""_3725.py

PointLoadCompoundStabilityAnalysis
"""


from typing import List

from mastapy.system_model.part_model import _2221
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3594
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3761
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'PointLoadCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundStabilityAnalysis',)


class PointLoadCompoundStabilityAnalysis(_3761.VirtualComponentCompoundStabilityAnalysis):
    """PointLoadCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _POINT_LOAD_COMPOUND_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'PointLoadCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2221.PointLoad':
        """PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3594.PointLoadStabilityAnalysis]':
        """List[PointLoadStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3594.PointLoadStabilityAnalysis]':
        """List[PointLoadStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
