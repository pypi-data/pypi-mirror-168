"""_3591.py

PlanetaryConnectionStabilityAnalysis
"""


from mastapy.system_model.connections_and_sockets import _2038
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6659
from mastapy.system_model.analyses_and_results.stability_analyses import _3605
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'PlanetaryConnectionStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionStabilityAnalysis',)


class PlanetaryConnectionStabilityAnalysis(_3605.ShaftToMountableComponentConnectionStabilityAnalysis):
    """PlanetaryConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _PLANETARY_CONNECTION_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2038.PlanetaryConnection':
        """PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6659.PlanetaryConnectionLoadCase':
        """PlanetaryConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
