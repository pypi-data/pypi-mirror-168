"""_5997.py

FlexiblePinAnalysisGearAndBearingRating
"""


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections.compound import _2644, _2680, _2603
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.flexible_pin_analyses import _5994
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ANALYSIS_GEAR_AND_BEARING_RATING = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'FlexiblePinAnalysisGearAndBearingRating')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAnalysisGearAndBearingRating',)


class FlexiblePinAnalysisGearAndBearingRating(_5994.FlexiblePinAnalysis):
    """FlexiblePinAnalysisGearAndBearingRating

    This is a mastapy class.
    """

    TYPE = _FLEXIBLE_PIN_ANALYSIS_GEAR_AND_BEARING_RATING

    def __init__(self, instance_to_wrap: 'FlexiblePinAnalysisGearAndBearingRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_analysis(self) -> '_2644.CylindricalGearSetCompoundSystemDeflection':
        """CylindricalGearSetCompoundSystemDeflection: 'GearSetAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetAnalysis

        if temp is None:
            return None

        if _2644.CylindricalGearSetCompoundSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_set_analysis to CylindricalGearSetCompoundSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_analyses(self) -> 'List[_2603.BearingCompoundSystemDeflection]':
        """List[BearingCompoundSystemDeflection]: 'BearingAnalyses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingAnalyses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
