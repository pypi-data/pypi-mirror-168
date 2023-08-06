"""_7058.py

FlexiblePinAssemblyAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model import _2204
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6612
from mastapy.system_model.analyses_and_results.system_deflections import _2502, _2522, _2545
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7097, _7047, _7100
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'FlexiblePinAssemblyAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyAdvancedSystemDeflection',)


class FlexiblePinAssemblyAdvancedSystemDeflection(_7100.SpecialisedAssemblyAdvancedSystemDeflection):
    """FlexiblePinAssemblyAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2204.FlexiblePinAssembly':
        """FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6612.FlexiblePinAssemblyLoadCase':
        """FlexiblePinAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2502.FlexiblePinAssemblySystemDeflection]':
        """List[FlexiblePinAssemblySystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblySystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def load_sharing_factor_reporters(self) -> 'List[_2522.LoadSharingFactorReporter]':
        """List[LoadSharingFactorReporter]: 'LoadSharingFactorReporters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingFactorReporters

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def pin_advanced_analyses(self) -> 'List[_7097.ShaftAdvancedSystemDeflection]':
        """List[ShaftAdvancedSystemDeflection]: 'PinAdvancedAnalyses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinAdvancedAnalyses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def pin_spindle_fit_advanced_analyses(self) -> 'List[_2545.ShaftHubConnectionSystemDeflection]':
        """List[ShaftHubConnectionSystemDeflection]: 'PinSpindleFitAdvancedAnalyses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinSpindleFitAdvancedAnalyses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planet_gear_analyses(self) -> 'List[_7047.CylindricalGearAdvancedSystemDeflection]':
        """List[CylindricalGearAdvancedSystemDeflection]: 'PlanetGearAnalyses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetGearAnalyses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spindle_advanced_analyses(self) -> 'List[_7097.ShaftAdvancedSystemDeflection]':
        """List[ShaftAdvancedSystemDeflection]: 'SpindleAdvancedAnalyses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpindleAdvancedAnalyses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
