"""_3516.py

BeltConnectionStabilityAnalysis
"""


from mastapy.system_model.connections_and_sockets import _2019, _2024
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6544, _6577
from mastapy.system_model.analyses_and_results.stability_analyses import _3573
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'BeltConnectionStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionStabilityAnalysis',)


class BeltConnectionStabilityAnalysis(_3573.InterMountableComponentConnectionStabilityAnalysis):
    """BeltConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _BELT_CONNECTION_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'BeltConnectionStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2019.BeltConnection':
        """BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2019.BeltConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BeltConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6544.BeltConnectionLoadCase':
        """BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        if _6544.BeltConnectionLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_load_case to BeltConnectionLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
