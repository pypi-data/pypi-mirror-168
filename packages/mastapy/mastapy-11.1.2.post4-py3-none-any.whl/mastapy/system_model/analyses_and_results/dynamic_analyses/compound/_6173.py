"""_6173.py

CVTCompoundDynamicAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.dynamic_analyses import _6043
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6142
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'CVTCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundDynamicAnalysis',)


class CVTCompoundDynamicAnalysis(_6142.BeltDriveCompoundDynamicAnalysis):
    """CVTCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'CVTCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6043.CVTDynamicAnalysis]':
        """List[CVTDynamicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6043.CVTDynamicAnalysis]':
        """List[CVTDynamicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
