"""_3528.py

ClutchConnectionStabilityAnalysis
"""


from mastapy.system_model.connections_and_sockets.couplings import _2093
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6556
from mastapy.system_model.analyses_and_results.stability_analyses import _3544
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ClutchConnectionStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionStabilityAnalysis',)


class ClutchConnectionStabilityAnalysis(_3544.CouplingConnectionStabilityAnalysis):
    """ClutchConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CLUTCH_CONNECTION_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'ClutchConnectionStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2093.ClutchConnection':
        """ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6556.ClutchConnectionLoadCase':
        """ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
