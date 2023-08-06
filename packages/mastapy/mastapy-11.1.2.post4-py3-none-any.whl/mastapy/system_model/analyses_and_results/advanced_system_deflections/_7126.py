"""_7126.py

WormGearAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.gears import _2300
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _346
from mastapy.system_model.analyses_and_results.static_loads import _6710
from mastapy.system_model.analyses_and_results.system_deflections import _2582
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7059
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'WormGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearAdvancedSystemDeflection',)


class WormGearAdvancedSystemDeflection(_7059.GearAdvancedSystemDeflection):
    """WormGearAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'WormGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2300.WormGear':
        """WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_detailed_analysis(self) -> '_346.WormGearRating':
        """WormGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDetailedAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6710.WormGearLoadCase':
        """WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2582.WormGearSystemDeflection]':
        """List[WormGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
