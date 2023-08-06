"""_5641.py

ConnectorCompoundHarmonicAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses import _5450
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5682
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'ConnectorCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundHarmonicAnalysis',)


class ConnectorCompoundHarmonicAnalysis(_5682.MountableComponentCompoundHarmonicAnalysis):
    """ConnectorCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _CONNECTOR_COMPOUND_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConnectorCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_5450.ConnectorHarmonicAnalysis]':
        """List[ConnectorHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_5450.ConnectorHarmonicAnalysis]':
        """List[ConnectorHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
