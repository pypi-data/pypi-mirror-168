"""_5646.py

CVTCompoundHarmonicAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses import _5455
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5615
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'CVTCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundHarmonicAnalysis',)


class CVTCompoundHarmonicAnalysis(_5615.BeltDriveCompoundHarmonicAnalysis):
    """CVTCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_COMPOUND_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'CVTCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5455.CVTHarmonicAnalysis]':
        """List[CVTHarmonicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5455.CVTHarmonicAnalysis]':
        """List[CVTHarmonicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
