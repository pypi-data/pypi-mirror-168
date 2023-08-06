"""_3609.py

SpiralBevelGearStabilityAnalysis
"""


from mastapy.system_model.part_model.gears import _2292
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6681
from mastapy.system_model.analyses_and_results.stability_analyses import _3525
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'SpiralBevelGearStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearStabilityAnalysis',)


class SpiralBevelGearStabilityAnalysis(_3525.BevelGearStabilityAnalysis):
    """SpiralBevelGearStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'SpiralBevelGearStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2292.SpiralBevelGear':
        """SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6681.SpiralBevelGearLoadCase':
        """SpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
