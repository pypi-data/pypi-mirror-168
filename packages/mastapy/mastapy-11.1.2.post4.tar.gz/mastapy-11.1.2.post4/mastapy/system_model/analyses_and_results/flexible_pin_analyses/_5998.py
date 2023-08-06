"""_5998.py

FlexiblePinAnalysisManufactureLevel
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4083
from mastapy.system_model.analyses_and_results.flexible_pin_analyses import _5994
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ANALYSIS_MANUFACTURE_LEVEL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'FlexiblePinAnalysisManufactureLevel')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAnalysisManufactureLevel',)


class FlexiblePinAnalysisManufactureLevel(_5994.FlexiblePinAnalysis):
    """FlexiblePinAnalysisManufactureLevel

    This is a mastapy class.
    """

    TYPE = _FLEXIBLE_PIN_ANALYSIS_MANUFACTURE_LEVEL

    def __init__(self, instance_to_wrap: 'FlexiblePinAnalysisManufactureLevel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def load_sharing_factors(self) -> 'List[float]':
        """List[float]: 'LoadSharingFactors' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingFactors

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def planetary_mesh_analysis(self) -> '_4083.CylindricalGearMeshParametricStudyTool':
        """CylindricalGearMeshParametricStudyTool: 'PlanetaryMeshAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetaryMeshAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
