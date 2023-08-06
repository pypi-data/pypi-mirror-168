"""_3880.py

SpringDamperHalfPowerFlow
"""


from mastapy.system_model.part_model.couplings import _2350
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6685
from mastapy.system_model.analyses_and_results.power_flows import _3812
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SpringDamperHalfPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfPowerFlow',)


class SpringDamperHalfPowerFlow(_3812.CouplingHalfPowerFlow):
    """SpringDamperHalfPowerFlow

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_HALF_POWER_FLOW

    def __init__(self, instance_to_wrap: 'SpringDamperHalfPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2350.SpringDamperHalf':
        """SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6685.SpringDamperHalfLoadCase':
        """SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
