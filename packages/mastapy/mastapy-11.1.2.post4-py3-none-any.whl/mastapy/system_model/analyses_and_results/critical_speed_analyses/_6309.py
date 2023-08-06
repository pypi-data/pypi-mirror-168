"""_6309.py

CVTBeltConnectionCriticalSpeedAnalysis
"""


from mastapy.system_model.connections_and_sockets import _2024
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6276
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'CVTBeltConnectionCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionCriticalSpeedAnalysis',)


class CVTBeltConnectionCriticalSpeedAnalysis(_6276.BeltConnectionCriticalSpeedAnalysis):
    """CVTBeltConnectionCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_BELT_CONNECTION_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2024.CVTBeltConnection':
        """CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
