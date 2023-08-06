"""_1041.py

TiffAnalysisSettings
"""


from mastapy._internal import constructor
from mastapy.math_utility import _1341
from mastapy.gears.gear_designs.cylindrical import _1012
from mastapy.utility import _1390
from mastapy._internal.python_net import python_net_import

_TIFF_ANALYSIS_SETTINGS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'TiffAnalysisSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('TiffAnalysisSettings',)


class TiffAnalysisSettings(_1390.IndependentReportablePropertiesBase['TiffAnalysisSettings']):
    """TiffAnalysisSettings

    This is a mastapy class.
    """

    TYPE = _TIFF_ANALYSIS_SETTINGS

    def __init__(self, instance_to_wrap: 'TiffAnalysisSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def include_findley_analysis(self) -> 'bool':
        """bool: 'IncludeFindleyAnalysis' is the original name of this property."""

        temp = self.wrapped.IncludeFindleyAnalysis

        if temp is None:
            return None

        return temp

    @include_findley_analysis.setter
    def include_findley_analysis(self, value: 'bool'):
        self.wrapped.IncludeFindleyAnalysis = bool(value) if value else False

    @property
    def include_residual_stresses(self) -> 'bool':
        """bool: 'IncludeResidualStresses' is the original name of this property."""

        temp = self.wrapped.IncludeResidualStresses

        if temp is None:
            return None

        return temp

    @include_residual_stresses.setter
    def include_residual_stresses(self, value: 'bool'):
        self.wrapped.IncludeResidualStresses = bool(value) if value else False

    @property
    def include_shot_peening(self) -> 'bool':
        """bool: 'IncludeShotPeening' is the original name of this property."""

        temp = self.wrapped.IncludeShotPeening

        if temp is None:
            return None

        return temp

    @include_shot_peening.setter
    def include_shot_peening(self, value: 'bool'):
        self.wrapped.IncludeShotPeening = bool(value) if value else False

    @property
    def measured_residual_stress_profile_property(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'MeasuredResidualStressProfileProperty' is the original name of this property."""

        temp = self.wrapped.MeasuredResidualStressProfileProperty

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measured_residual_stress_profile_property.setter
    def measured_residual_stress_profile_property(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.MeasuredResidualStressProfileProperty = value

    @property
    def number_of_rotations_for_findley(self) -> 'int':
        """int: 'NumberOfRotationsForFindley' is the original name of this property."""

        temp = self.wrapped.NumberOfRotationsForFindley

        if temp is None:
            return None

        return temp

    @number_of_rotations_for_findley.setter
    def number_of_rotations_for_findley(self, value: 'int'):
        self.wrapped.NumberOfRotationsForFindley = int(value) if value else 0

    @property
    def shot_peening_depth(self) -> 'float':
        """float: 'ShotPeeningDepth' is the original name of this property."""

        temp = self.wrapped.ShotPeeningDepth

        if temp is None:
            return None

        return temp

    @shot_peening_depth.setter
    def shot_peening_depth(self, value: 'float'):
        self.wrapped.ShotPeeningDepth = float(value) if value else 0.0

    @property
    def shot_peening_factor(self) -> 'float':
        """float: 'ShotPeeningFactor' is the original name of this property."""

        temp = self.wrapped.ShotPeeningFactor

        if temp is None:
            return None

        return temp

    @shot_peening_factor.setter
    def shot_peening_factor(self, value: 'float'):
        self.wrapped.ShotPeeningFactor = float(value) if value else 0.0

    @property
    def strain_at_mid_case_depth(self) -> 'float':
        """float: 'StrainAtMidCaseDepth' is the original name of this property."""

        temp = self.wrapped.StrainAtMidCaseDepth

        if temp is None:
            return None

        return temp

    @strain_at_mid_case_depth.setter
    def strain_at_mid_case_depth(self, value: 'float'):
        self.wrapped.StrainAtMidCaseDepth = float(value) if value else 0.0

    @property
    def strain_at_surface(self) -> 'float':
        """float: 'StrainAtSurface' is the original name of this property."""

        temp = self.wrapped.StrainAtSurface

        if temp is None:
            return None

        return temp

    @strain_at_surface.setter
    def strain_at_surface(self, value: 'float'):
        self.wrapped.StrainAtSurface = float(value) if value else 0.0

    @property
    def core_material_properties(self) -> '_1012.HardenedMaterialProperties':
        """HardenedMaterialProperties: 'CoreMaterialProperties' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoreMaterialProperties

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def surface_material_properties(self) -> '_1012.HardenedMaterialProperties':
        """HardenedMaterialProperties: 'SurfaceMaterialProperties' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceMaterialProperties

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
