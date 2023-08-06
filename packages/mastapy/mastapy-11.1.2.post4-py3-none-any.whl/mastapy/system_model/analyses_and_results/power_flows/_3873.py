"""_3873.py

ShaftPowerFlow
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model.shaft_model import _2232
from mastapy.system_model.analyses_and_results.static_loads import _6677
from mastapy.system_model.analyses_and_results.power_flows import _3776
from mastapy._internal.python_net import python_net_import

_SHAFT_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ShaftPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftPowerFlow',)


class ShaftPowerFlow(_3776.AbstractShaftPowerFlow):
    """ShaftPowerFlow

    This is a mastapy class.
    """

    TYPE = _SHAFT_POWER_FLOW

    def __init__(self, instance_to_wrap: 'ShaftPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pin_tangential_oscillation_frequency(self) -> 'float':
        """float: 'PinTangentialOscillationFrequency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinTangentialOscillationFrequency

        if temp is None:
            return None

        return temp

    @property
    def component_design(self) -> '_2232.Shaft':
        """Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6677.ShaftLoadCase':
        """ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
