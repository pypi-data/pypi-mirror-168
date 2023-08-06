"""_6153.py

ClutchCompoundDynamicAnalysis
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2327
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6024
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6169
from mastapy._internal.python_net import python_net_import

_CLUTCH_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ClutchCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchCompoundDynamicAnalysis',)


class ClutchCompoundDynamicAnalysis(_6169.CouplingCompoundDynamicAnalysis):
    """ClutchCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _CLUTCH_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'ClutchCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2327.Clutch':
        """Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2327.Clutch':
        """Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6024.ClutchDynamicAnalysis]':
        """List[ClutchDynamicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6024.ClutchDynamicAnalysis]':
        """List[ClutchDynamicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
