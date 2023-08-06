"""_3600.py

RollingRingConnectionStabilityAnalysis
"""


from typing import List

from mastapy.system_model.connections_and_sockets import _2043
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6673
from mastapy.system_model.analyses_and_results.stability_analyses import _3573
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'RollingRingConnectionStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionStabilityAnalysis',)


class RollingRingConnectionStabilityAnalysis(_3573.InterMountableComponentConnectionStabilityAnalysis):
    """RollingRingConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _ROLLING_RING_CONNECTION_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'RollingRingConnectionStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2043.RollingRingConnection':
        """RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6673.RollingRingConnectionLoadCase':
        """RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionStabilityAnalysis]':
        """List[RollingRingConnectionStabilityAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
