"""_5995.py

FlexiblePinAnalysisConceptLevel
"""


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections import _2502, _2442
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.flexible_pin_analyses import _5994
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ANALYSIS_CONCEPT_LEVEL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'FlexiblePinAnalysisConceptLevel')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAnalysisConceptLevel',)


class FlexiblePinAnalysisConceptLevel(_5994.FlexiblePinAnalysis):
    """FlexiblePinAnalysisConceptLevel

    This is a mastapy class.
    """

    TYPE = _FLEXIBLE_PIN_ANALYSIS_CONCEPT_LEVEL

    def __init__(self, instance_to_wrap: 'FlexiblePinAnalysisConceptLevel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def flexible_pin_extreme_load_case(self) -> '_2502.FlexiblePinAssemblySystemDeflection':
        """FlexiblePinAssemblySystemDeflection: 'FlexiblePinExtremeLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlexiblePinExtremeLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def flexible_pin_nominal_load_case(self) -> '_2502.FlexiblePinAssemblySystemDeflection':
        """FlexiblePinAssemblySystemDeflection: 'FlexiblePinNominalLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlexiblePinNominalLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planet_bearings_in_nominal_load(self) -> 'List[_2442.BearingSystemDeflection]':
        """List[BearingSystemDeflection]: 'PlanetBearingsInNominalLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetBearingsInNominalLoad

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
