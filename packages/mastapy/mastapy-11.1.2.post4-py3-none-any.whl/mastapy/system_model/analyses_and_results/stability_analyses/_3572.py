"""_3572.py

HypoidGearStabilityAnalysis
"""


from mastapy.system_model.part_model.gears import _2283
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6631
from mastapy.system_model.analyses_and_results.stability_analyses import _3513
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'HypoidGearStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearStabilityAnalysis',)


class HypoidGearStabilityAnalysis(_3513.AGMAGleasonConicalGearStabilityAnalysis):
    """HypoidGearStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'HypoidGearStabilityAnalysis.TYPE'):
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
