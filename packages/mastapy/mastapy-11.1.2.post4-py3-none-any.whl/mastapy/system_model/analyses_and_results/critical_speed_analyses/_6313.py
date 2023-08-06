"""_6313.py

CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis
"""


from mastapy.system_model.connections_and_sockets.cycloidal import _2086
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6291
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis',)


class CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis(_6291.CoaxialConnectionCriticalSpeedAnalysis):
    """CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2086.CycloidalDiscCentralBearingConnection':
        """CycloidalDiscCentralBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
