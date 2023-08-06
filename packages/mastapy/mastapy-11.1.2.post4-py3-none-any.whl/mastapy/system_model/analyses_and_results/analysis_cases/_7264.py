"""_7264.py

ConnectionAnalysisCase
"""


from mastapy.system_model.analyses_and_results import _2398
from mastapy._internal.python_net import python_net_import

_CONNECTION_ANALYSIS_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases', 'ConnectionAnalysisCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionAnalysisCase',)


class ConnectionAnalysisCase(_2398.ConnectionAnalysis):
    """ConnectionAnalysisCase

    This is a mastapy class.
    """

    TYPE = _CONNECTION_ANALYSIS_CASE

    def __init__(self, instance_to_wrap: 'ConnectionAnalysisCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
