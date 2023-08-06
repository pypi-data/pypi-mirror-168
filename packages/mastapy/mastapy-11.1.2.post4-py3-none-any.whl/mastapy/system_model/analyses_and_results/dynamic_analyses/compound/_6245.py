"""_6245.py

SynchroniserCompoundDynamicAnalysis
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2351
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6116
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6230
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'SynchroniserCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundDynamicAnalysis',)


class SynchroniserCompoundDynamicAnalysis(_6230.SpecialisedAssemblyCompoundDynamicAnalysis):
    """SynchroniserCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2351.Synchroniser':
        """Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2351.Synchroniser':
        """Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6116.SynchroniserDynamicAnalysis]':
        """List[SynchroniserDynamicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6116.SynchroniserDynamicAnalysis]':
        """List[SynchroniserDynamicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
