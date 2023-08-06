"""_3838.py

HypoidGearPowerFlow
"""


from mastapy.system_model.part_model.gears import _2283
from mastapy._internal import constructor
from mastapy.gears.rating.hypoid import _411
from mastapy.system_model.analyses_and_results.static_loads import _6631
from mastapy.system_model.analyses_and_results.power_flows import _3779
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'HypoidGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearPowerFlow',)


class HypoidGearPowerFlow(_3779.AGMAGleasonConicalGearPowerFlow):
    """HypoidGearPowerFlow

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_POWER_FLOW

    def __init__(self, instance_to_wrap: 'HypoidGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2283.HypoidGear':
        """HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_detailed_analysis(self) -> '_411.HypoidGearRating':
        """HypoidGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDetailedAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6631.HypoidGearLoadCase':
        """HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
