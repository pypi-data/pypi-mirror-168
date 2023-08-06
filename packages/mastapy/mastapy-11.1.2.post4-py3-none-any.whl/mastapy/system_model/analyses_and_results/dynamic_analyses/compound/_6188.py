"""_6188.py

FEPartCompoundDynamicAnalysis
"""


from typing import List

from mastapy.system_model.part_model import _2203
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6059
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6134
from mastapy._internal.python_net import python_net_import

_FE_PART_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'FEPartCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartCompoundDynamicAnalysis',)


class FEPartCompoundDynamicAnalysis(_6134.AbstractShaftOrHousingCompoundDynamicAnalysis):
    """FEPartCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _FE_PART_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'FEPartCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2203.FEPart':
        """FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6059.FEPartDynamicAnalysis]':
        """List[FEPartDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[FEPartCompoundDynamicAnalysis]':
        """List[FEPartCompoundDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6059.FEPartDynamicAnalysis]':
        """List[FEPartDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
