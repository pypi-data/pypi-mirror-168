"""_5656.py

DatumCompoundHarmonicAnalysis
"""


from typing import List

from mastapy.system_model.part_model import _2199
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5465
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5630
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'DatumCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundHarmonicAnalysis',)


class DatumCompoundHarmonicAnalysis(_5630.ComponentCompoundHarmonicAnalysis):
    """DatumCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _DATUM_COMPOUND_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'DatumCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2199.Datum':
        """Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5465.DatumHarmonicAnalysis]':
        """List[DatumHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5465.DatumHarmonicAnalysis]':
        """List[DatumHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
