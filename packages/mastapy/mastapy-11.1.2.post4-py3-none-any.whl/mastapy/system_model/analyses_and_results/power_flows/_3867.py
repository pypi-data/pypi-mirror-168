"""_3867.py

RingPinsToDiscConnectionPowerFlow
"""


from mastapy.system_model.connections_and_sockets.cycloidal import _2092
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6671
from mastapy.system_model.analyses_and_results.power_flows import _3840
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'RingPinsToDiscConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionPowerFlow',)


class RingPinsToDiscConnectionPowerFlow(_3840.InterMountableComponentConnectionPowerFlow):
    """RingPinsToDiscConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE = _RING_PINS_TO_DISC_CONNECTION_POWER_FLOW

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2092.RingPinsToDiscConnection':
        """RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6671.RingPinsToDiscConnectionLoadCase':
        """RingPinsToDiscConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
