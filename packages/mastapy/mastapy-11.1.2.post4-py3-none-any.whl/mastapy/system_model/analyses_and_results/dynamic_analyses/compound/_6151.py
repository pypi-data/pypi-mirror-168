"""_6151.py

BoltCompoundDynamicAnalysis
"""


from typing import List

from mastapy.system_model.part_model import _2193
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6021
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6157
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'BoltCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundDynamicAnalysis',)


class BoltCompoundDynamicAnalysis(_6157.ComponentCompoundDynamicAnalysis):
    """BoltCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _BOLT_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'BoltCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2193.Bolt':
        """Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6021.BoltDynamicAnalysis]':
        """List[BoltDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6021.BoltDynamicAnalysis]':
        """List[BoltDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
