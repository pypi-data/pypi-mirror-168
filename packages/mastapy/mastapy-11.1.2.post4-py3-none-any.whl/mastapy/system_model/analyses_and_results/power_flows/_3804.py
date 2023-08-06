"""_3804.py

ConceptGearPowerFlow
"""


from mastapy.system_model.part_model.gears import _2270
from mastapy._internal import constructor
from mastapy.gears.rating.concept import _517
from mastapy.system_model.analyses_and_results.static_loads import _6564
from mastapy.system_model.analyses_and_results.power_flows import _3834
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ConceptGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearPowerFlow',)


class ConceptGearPowerFlow(_3834.GearPowerFlow):
    """ConceptGearPowerFlow

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_POWER_FLOW

    def __init__(self, instance_to_wrap: 'ConceptGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2270.ConceptGear':
        """ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_detailed_analysis(self) -> '_517.ConceptGearRating':
        """ConceptGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDetailedAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6564.ConceptGearLoadCase':
        """ConceptGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
