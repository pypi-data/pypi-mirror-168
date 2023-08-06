"""_3870.py

RollingRingPowerFlow
"""


from mastapy.system_model.part_model.couplings import _2345
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6674
from mastapy.system_model.analyses_and_results.power_flows import _3812
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'RollingRingPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingPowerFlow',)


class RollingRingPowerFlow(_3812.CouplingHalfPowerFlow):
    """RollingRingPowerFlow

    This is a mastapy class.
    """

    TYPE = _ROLLING_RING_POWER_FLOW

    def __init__(self, instance_to_wrap: 'RollingRingPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2345.RollingRing':
        """RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6674.RollingRingLoadCase':
        """RollingRingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
