"""_3676.py

CouplingCompoundStabilityAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.stability_analyses import _3546
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3737
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'CouplingCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundStabilityAnalysis',)


class CouplingCompoundStabilityAnalysis(_3737.SpecialisedAssemblyCompoundStabilityAnalysis):
    """CouplingCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _COUPLING_COMPOUND_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'CouplingCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(self) -> 'List[_3546.CouplingStabilityAnalysis]':
        """List[CouplingStabilityAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3546.CouplingStabilityAnalysis]':
        """List[CouplingStabilityAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
