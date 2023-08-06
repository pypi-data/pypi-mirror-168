"""_3761.py

VirtualComponentCompoundStabilityAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.stability_analyses import _3632
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3716
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'VirtualComponentCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundStabilityAnalysis',)


class VirtualComponentCompoundStabilityAnalysis(_3716.MountableComponentCompoundStabilityAnalysis):
    """VirtualComponentCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_3632.VirtualComponentStabilityAnalysis]':
        """List[VirtualComponentStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_3632.VirtualComponentStabilityAnalysis]':
        """List[VirtualComponentStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
