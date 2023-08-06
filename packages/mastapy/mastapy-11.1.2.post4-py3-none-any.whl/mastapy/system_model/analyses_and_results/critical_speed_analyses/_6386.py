"""_6386.py

TorqueConverterConnectionCriticalSpeedAnalysis
"""


from mastapy.system_model.connections_and_sockets.couplings import _2103
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6700
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6304
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'TorqueConverterConnectionCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionCriticalSpeedAnalysis',)


class TorqueConverterConnectionCriticalSpeedAnalysis(_6304.CouplingConnectionCriticalSpeedAnalysis):
    """TorqueConverterConnectionCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_CONNECTION_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2103.TorqueConverterConnection':
        """TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6700.TorqueConverterConnectionLoadCase':
        """TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
