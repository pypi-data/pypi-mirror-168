"""_3593.py

PlanetCarrierStabilityAnalysis
"""


from mastapy.system_model.part_model import _2219
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6662
from mastapy.system_model.analyses_and_results.stability_analyses import _3585
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'PlanetCarrierStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierStabilityAnalysis',)


class PlanetCarrierStabilityAnalysis(_3585.MountableComponentStabilityAnalysis):
    """PlanetCarrierStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _PLANET_CARRIER_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'PlanetCarrierStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2219.PlanetCarrier':
        """PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6662.PlanetCarrierLoadCase':
        """PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
