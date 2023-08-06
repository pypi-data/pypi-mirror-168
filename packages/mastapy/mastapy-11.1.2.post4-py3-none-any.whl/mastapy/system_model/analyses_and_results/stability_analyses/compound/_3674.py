"""_3674.py

ConnectionCompoundStabilityAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.stability_analyses import _3542
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.analysis_cases import _7265
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ConnectionCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundStabilityAnalysis',)


class ConnectionCompoundStabilityAnalysis(_7265.ConnectionCompoundAnalysis):
    """ConnectionCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CONNECTION_COMPOUND_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConnectionCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(self) -> 'List[_3542.ConnectionStabilityAnalysis]':
        """List[ConnectionStabilityAnalysis]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3542.ConnectionStabilityAnalysis]':
        """List[ConnectionStabilityAnalysis]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
