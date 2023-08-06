"""_6227.py

ShaftCompoundDynamicAnalysis
"""


from typing import List

from mastapy.system_model.part_model.shaft_model import _2232
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6098
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6133
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ShaftCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundDynamicAnalysis',)


class ShaftCompoundDynamicAnalysis(_6133.AbstractShaftCompoundDynamicAnalysis):
    """ShaftCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _SHAFT_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'ShaftCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2232.Shaft':
        """Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6098.ShaftDynamicAnalysis]':
        """List[ShaftDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundDynamicAnalysis]':
        """List[ShaftCompoundDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6098.ShaftDynamicAnalysis]':
        """List[ShaftDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
