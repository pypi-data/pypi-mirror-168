"""_6088.py

PlanetCarrierDynamicAnalysis
"""


from mastapy.system_model.part_model import _2219
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6662
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6080
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'PlanetCarrierDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierDynamicAnalysis',)


class PlanetCarrierDynamicAnalysis(_6080.MountableComponentDynamicAnalysis):
    """PlanetCarrierDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _PLANET_CARRIER_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'PlanetCarrierDynamicAnalysis.TYPE'):
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
