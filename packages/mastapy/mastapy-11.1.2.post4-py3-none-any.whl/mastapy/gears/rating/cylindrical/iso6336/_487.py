"""_487.py

ISO6336AbstractMetalMeshSingleFlankRating
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.rating.cylindrical import (
    _444, _448, _449, _428
)
from mastapy.gears.gear_designs.cylindrical import _1034
from mastapy.gears.rating.cylindrical.iso6336 import (
    _481, _483, _486, _485
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ISO6336_ABSTRACT_METAL_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ISO6336AbstractMetalMeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO6336AbstractMetalMeshSingleFlankRating',)


class ISO6336AbstractMetalMeshSingleFlankRating(_485.ISO6336AbstractMeshSingleFlankRating):
    """ISO6336AbstractMetalMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _ISO6336_ABSTRACT_METAL_MESH_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'ISO6336AbstractMetalMeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allowable_stress_number_contact(self) -> 'float':
        """float: 'AllowableStressNumberContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableStressNumberContact

        if temp is None:
            return None

        return temp

    @property
    def angle_factor(self) -> 'float':
        """float: 'AngleFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngleFactor

        if temp is None:
            return None

        return temp

    @property
    def approach_factor_integral(self) -> 'float':
        """float: 'ApproachFactorIntegral' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ApproachFactorIntegral

        if temp is None:
            return None

        return temp

    @property
    def approach_factor_of_maximum_flash_temperature(self) -> 'float':
        """float: 'ApproachFactorOfMaximumFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ApproachFactorOfMaximumFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def average_flash_temperature(self) -> 'float':
        """float: 'AverageFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def basic_mean_flash_temperature(self) -> 'float':
        """float: 'BasicMeanFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicMeanFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def basic_rack_factor(self) -> 'float':
        """float: 'BasicRackFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicRackFactor

        if temp is None:
            return None

        return temp

    @property
    def bulk_temperature_for_micropitting(self) -> 'float':
        """float: 'BulkTemperatureForMicropitting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BulkTemperatureForMicropitting

        if temp is None:
            return None

        return temp

    @property
    def bulk_tooth_temperature_flash_temperature_method(self) -> 'float':
        """float: 'BulkToothTemperatureFlashTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BulkToothTemperatureFlashTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def bulk_tooth_temperature_integral_temperature_method(self) -> 'float':
        """float: 'BulkToothTemperatureIntegralTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BulkToothTemperatureIntegralTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def contact_exposure_time_flash_temperature_method(self) -> 'float':
        """float: 'ContactExposureTimeFlashTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactExposureTimeFlashTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def contact_exposure_time_integral_temperature_method(self) -> 'float':
        """float: 'ContactExposureTimeIntegralTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactExposureTimeIntegralTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def contact_ratio_factor(self) -> 'float':
        """float: 'ContactRatioFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactRatioFactor

        if temp is None:
            return None

        return temp

    @property
    def contact_time_at_high_velocity(self) -> 'float':
        """float: 'ContactTimeAtHighVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactTimeAtHighVelocity

        if temp is None:
            return None

        return temp

    @property
    def contact_time_at_medium_velocity(self) -> 'float':
        """float: 'ContactTimeAtMediumVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactTimeAtMediumVelocity

        if temp is None:
            return None

        return temp

    @property
    def drive_gear_tip_relief(self) -> 'float':
        """float: 'DriveGearTipRelief' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DriveGearTipRelief

        if temp is None:
            return None

        return temp

    @property
    def dynamic_factor_source(self) -> 'str':
        """str: 'DynamicFactorSource' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicFactorSource

        if temp is None:
            return None

        return temp

    @property
    def effective_equivalent_misalignment(self) -> 'float':
        """float: 'EffectiveEquivalentMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveEquivalentMisalignment

        if temp is None:
            return None

        return temp

    @property
    def effective_profile_form_deviation(self) -> 'float':
        """float: 'EffectiveProfileFormDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveProfileFormDeviation

        if temp is None:
            return None

        return temp

    @property
    def effective_tip_relief(self) -> 'float':
        """float: 'EffectiveTipRelief' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveTipRelief

        if temp is None:
            return None

        return temp

    @property
    def effective_transverse_base_pitch_deviation(self) -> 'float':
        """float: 'EffectiveTransverseBasePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveTransverseBasePitchDeviation

        if temp is None:
            return None

        return temp

    @property
    def equivalent_misalignment_due_to_system_deflection(self) -> 'float':
        """float: 'EquivalentMisalignmentDueToSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EquivalentMisalignmentDueToSystemDeflection

        if temp is None:
            return None

        return temp

    @property
    def equivalent_tip_relief_of_pinion(self) -> 'float':
        """float: 'EquivalentTipReliefOfPinion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EquivalentTipReliefOfPinion

        if temp is None:
            return None

        return temp

    @property
    def equivalent_tip_relief_of_wheel(self) -> 'float':
        """float: 'EquivalentTipReliefOfWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EquivalentTipReliefOfWheel

        if temp is None:
            return None

        return temp

    @property
    def face_load_factor_bending(self) -> 'float':
        """float: 'FaceLoadFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceLoadFactorBending

        if temp is None:
            return None

        return temp

    @property
    def face_load_factor_contact_source(self) -> 'str':
        """str: 'FaceLoadFactorContactSource' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceLoadFactorContactSource

        if temp is None:
            return None

        return temp

    @property
    def gear_blank_factor(self) -> 'float':
        """float: 'GearBlankFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBlankFactor

        if temp is None:
            return None

        return temp

    @property
    def geometry_factor_at_pinion_tooth_tip(self) -> 'float':
        """float: 'GeometryFactorAtPinionToothTip' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactorAtPinionToothTip

        if temp is None:
            return None

        return temp

    @property
    def helical_load_factor(self) -> 'float':
        """float: 'HelicalLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelicalLoadFactor

        if temp is None:
            return None

        return temp

    @property
    def highest_local_contact_temperature(self) -> 'float':
        """float: 'HighestLocalContactTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HighestLocalContactTemperature

        if temp is None:
            return None

        return temp

    @property
    def initial_equivalent_misalignment(self) -> 'float':
        """float: 'InitialEquivalentMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InitialEquivalentMisalignment

        if temp is None:
            return None

        return temp

    @property
    def integral_contact_temperature(self) -> 'float':
        """float: 'IntegralContactTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IntegralContactTemperature

        if temp is None:
            return None

        return temp

    @property
    def integral_scuffing_temperature(self) -> 'float':
        """float: 'IntegralScuffingTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IntegralScuffingTemperature

        if temp is None:
            return None

        return temp

    @property
    def length_of_path_of_contact(self) -> 'float':
        """float: 'LengthOfPathOfContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfPathOfContact

        if temp is None:
            return None

        return temp

    @property
    def limiting_specific_lubricant_film_thickness_of_the_test_gears(self) -> 'float':
        """float: 'LimitingSpecificLubricantFilmThicknessOfTheTestGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LimitingSpecificLubricantFilmThicknessOfTheTestGears

        if temp is None:
            return None

        return temp

    @property
    def load_losses_factor(self) -> 'float':
        """float: 'LoadLossesFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadLossesFactor

        if temp is None:
            return None

        return temp

    @property
    def local_hertzian_contact_stress_calculation_method(self) -> 'str':
        """str: 'LocalHertzianContactStressCalculationMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LocalHertzianContactStressCalculationMethod

        if temp is None:
            return None

        return temp

    @property
    def longest_contact_exposure_time(self) -> 'float':
        """float: 'LongestContactExposureTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LongestContactExposureTime

        if temp is None:
            return None

        return temp

    @property
    def longest_contact_exposure_time_integral(self) -> 'float':
        """float: 'LongestContactExposureTimeIntegral' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LongestContactExposureTimeIntegral

        if temp is None:
            return None

        return temp

    @property
    def lubricant_density_at_156_degrees_celsius(self) -> 'float':
        """float: 'LubricantDensityAt156DegreesCelsius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricantDensityAt156DegreesCelsius

        if temp is None:
            return None

        return temp

    @property
    def lubricant_density_at_bulk_tooth_temperature(self) -> 'float':
        """float: 'LubricantDensityAtBulkToothTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricantDensityAtBulkToothTemperature

        if temp is None:
            return None

        return temp

    @property
    def lubricant_density_at_micropitting_bulk_tooth_temperature(self) -> 'float':
        """float: 'LubricantDensityAtMicropittingBulkToothTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricantDensityAtMicropittingBulkToothTemperature

        if temp is None:
            return None

        return temp

    @property
    def lubricant_dynamic_viscosity_at_tooth_temperature_micropitting(self) -> 'float':
        """float: 'LubricantDynamicViscosityAtToothTemperatureMicropitting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricantDynamicViscosityAtToothTemperatureMicropitting

        if temp is None:
            return None

        return temp

    @property
    def lubricant_factor_flash(self) -> 'float':
        """float: 'LubricantFactorFlash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricantFactorFlash

        if temp is None:
            return None

        return temp

    @property
    def lubricant_factor_integral(self) -> 'float':
        """float: 'LubricantFactorIntegral' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricantFactorIntegral

        if temp is None:
            return None

        return temp

    @property
    def lubrication_system_factor(self) -> 'float':
        """float: 'LubricationSystemFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricationSystemFactor

        if temp is None:
            return None

        return temp

    @property
    def material_factor(self) -> 'float':
        """float: 'MaterialFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaterialFactor

        if temp is None:
            return None

        return temp

    @property
    def material_parameter(self) -> 'float':
        """float: 'MaterialParameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaterialParameter

        if temp is None:
            return None

        return temp

    @property
    def maximum_base_pitch_deviation(self) -> 'float':
        """float: 'MaximumBasePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumBasePitchDeviation

        if temp is None:
            return None

        return temp

    @property
    def maximum_contact_temperature(self) -> 'float':
        """float: 'MaximumContactTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumContactTemperature

        if temp is None:
            return None

        return temp

    @property
    def maximum_flash_temperature(self) -> 'float':
        """float: 'MaximumFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def maximum_profile_form_deviation(self) -> 'float':
        """float: 'MaximumProfileFormDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumProfileFormDeviation

        if temp is None:
            return None

        return temp

    @property
    def mean_coefficient_of_friction_integral_temperature_method(self) -> 'float':
        """float: 'MeanCoefficientOfFrictionIntegralTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanCoefficientOfFrictionIntegralTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def mean_coefficient_of_friction_calculated_constant_flash_temperature_method(self) -> 'float':
        """float: 'MeanCoefficientOfFrictionCalculatedConstantFlashTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanCoefficientOfFrictionCalculatedConstantFlashTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def mean_flash_temperature(self) -> 'float':
        """float: 'MeanFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def mesh_misalignment_due_to_manufacturing_deviations(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MeshMisalignmentDueToManufacturingDeviations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshMisalignmentDueToManufacturingDeviations

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def mesh_stiffness(self) -> 'float':
        """float: 'MeshStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshStiffness

        if temp is None:
            return None

        return temp

    @property
    def micro_geometry_factor_for_the_dynamic_load(self) -> 'float':
        """float: 'MicroGeometryFactorForTheDynamicLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicroGeometryFactorForTheDynamicLoad

        if temp is None:
            return None

        return temp

    @property
    def micropitting_rating_method(self) -> '_444.MicropittingRatingMethod':
        """MicropittingRatingMethod: 'MicropittingRatingMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingRatingMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_444.MicropittingRatingMethod)(value) if value is not None else None

    @property
    def micropitting_safety_factor(self) -> 'float':
        """float: 'MicropittingSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def minimum_lubricant_film_thickness(self) -> 'float':
        """float: 'MinimumLubricantFilmThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricantFilmThickness

        if temp is None:
            return None

        return temp

    @property
    def minimum_specific_lubricant_film_thickness_in_the_contact_area(self) -> 'float':
        """float: 'MinimumSpecificLubricantFilmThicknessInTheContactArea' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumSpecificLubricantFilmThicknessInTheContactArea

        if temp is None:
            return None

        return temp

    @property
    def misalignment_due_to_micro_geometry_lead_relief(self) -> 'float':
        """float: 'MisalignmentDueToMicroGeometryLeadRelief' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentDueToMicroGeometryLeadRelief

        if temp is None:
            return None

        return temp

    @property
    def multiple_path_factor(self) -> 'float':
        """float: 'MultiplePathFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MultiplePathFactor

        if temp is None:
            return None

        return temp

    @property
    def normal_relative_radius_of_curvature_at_pitch_point_integral_temperature_method(self) -> 'float':
        """float: 'NormalRelativeRadiusOfCurvatureAtPitchPointIntegralTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalRelativeRadiusOfCurvatureAtPitchPointIntegralTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def normal_unit_load(self) -> 'float':
        """float: 'NormalUnitLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalUnitLoad

        if temp is None:
            return None

        return temp

    @property
    def optimal_tip_relief(self) -> 'float':
        """float: 'OptimalTipRelief' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OptimalTipRelief

        if temp is None:
            return None

        return temp

    @property
    def permissible_specific_lubricant_film_thickness(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PermissibleSpecificLubricantFilmThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleSpecificLubricantFilmThickness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def permissible_specific_lubricant_film_thickness_from_figure_a1(self) -> 'float':
        """float: 'PermissibleSpecificLubricantFilmThicknessFromFigureA1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleSpecificLubricantFilmThicknessFromFigureA1

        if temp is None:
            return None

        return temp

    @property
    def pressure_viscosity_coefficient_at_38_degrees_c(self) -> 'float':
        """float: 'PressureViscosityCoefficientAt38DegreesC' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureViscosityCoefficientAt38DegreesC

        if temp is None:
            return None

        return temp

    @property
    def pressure_viscosity_coefficient_at_bulk_temperature(self) -> 'float':
        """float: 'PressureViscosityCoefficientAtBulkTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureViscosityCoefficientAtBulkTemperature

        if temp is None:
            return None

        return temp

    @property
    def profile_form_deviation_factor_for_the_dynamic_load(self) -> 'float':
        """float: 'ProfileFormDeviationFactorForTheDynamicLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileFormDeviationFactorForTheDynamicLoad

        if temp is None:
            return None

        return temp

    @property
    def relative_mass_per_unit_face_width(self) -> 'float':
        """float: 'RelativeMassPerUnitFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeMassPerUnitFaceWidth

        if temp is None:
            return None

        return temp

    @property
    def relative_welding_factor(self) -> 'float':
        """float: 'RelativeWeldingFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeWeldingFactor

        if temp is None:
            return None

        return temp

    @property
    def resonance_ratio(self) -> 'float':
        """float: 'ResonanceRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResonanceRatio

        if temp is None:
            return None

        return temp

    @property
    def resonance_ratio_in_the_main_resonance_range(self) -> 'float':
        """float: 'ResonanceRatioInTheMainResonanceRange' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResonanceRatioInTheMainResonanceRange

        if temp is None:
            return None

        return temp

    @property
    def resonance_speed(self) -> 'float':
        """float: 'ResonanceSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResonanceSpeed

        if temp is None:
            return None

        return temp

    @property
    def roughness_factor_micropitting(self) -> 'float':
        """float: 'RoughnessFactorMicropitting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoughnessFactorMicropitting

        if temp is None:
            return None

        return temp

    @property
    def run_in_factor(self) -> 'float':
        """float: 'RunInFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RunInFactor

        if temp is None:
            return None

        return temp

    @property
    def run_in_grade(self) -> 'int':
        """int: 'RunInGrade' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RunInGrade

        if temp is None:
            return None

        return temp

    @property
    def running_in(self) -> 'float':
        """float: 'RunningIn' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RunningIn

        if temp is None:
            return None

        return temp

    @property
    def running_in_profile_form_deviation(self) -> 'float':
        """float: 'RunningInProfileFormDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RunningInProfileFormDeviation

        if temp is None:
            return None

        return temp

    @property
    def running_in_allowance_equivalent_misalignment(self) -> 'float':
        """float: 'RunningInAllowanceEquivalentMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RunningInAllowanceEquivalentMisalignment

        if temp is None:
            return None

        return temp

    @property
    def scuffing_load_safety_factor_integral_temperature_method(self) -> 'float':
        """float: 'ScuffingLoadSafetyFactorIntegralTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingLoadSafetyFactorIntegralTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def scuffing_rating_method_flash_temperature_method(self) -> '_448.ScuffingFlashTemperatureRatingMethod':
        """ScuffingFlashTemperatureRatingMethod: 'ScuffingRatingMethodFlashTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingRatingMethodFlashTemperatureMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_448.ScuffingFlashTemperatureRatingMethod)(value) if value is not None else None

    @property
    def scuffing_rating_method_integral_temperature_method(self) -> '_449.ScuffingIntegralTemperatureRatingMethod':
        """ScuffingIntegralTemperatureRatingMethod: 'ScuffingRatingMethodIntegralTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingRatingMethodIntegralTemperatureMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_449.ScuffingIntegralTemperatureRatingMethod)(value) if value is not None else None

    @property
    def scuffing_safety_factor_flash_temperature_method(self) -> 'float':
        """float: 'ScuffingSafetyFactorFlashTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorFlashTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def scuffing_safety_factor_integral_temperature_method(self) -> 'float':
        """float: 'ScuffingSafetyFactorIntegralTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorIntegralTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def scuffing_temperature(self) -> 'float':
        """float: 'ScuffingTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingTemperature

        if temp is None:
            return None

        return temp

    @property
    def scuffing_temperature_at_high_velocity(self) -> 'float':
        """float: 'ScuffingTemperatureAtHighVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingTemperatureAtHighVelocity

        if temp is None:
            return None

        return temp

    @property
    def scuffing_temperature_at_medium_velocity(self) -> 'float':
        """float: 'ScuffingTemperatureAtMediumVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingTemperatureAtMediumVelocity

        if temp is None:
            return None

        return temp

    @property
    def scuffing_temperature_gradient(self) -> 'float':
        """float: 'ScuffingTemperatureGradient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingTemperatureGradient

        if temp is None:
            return None

        return temp

    @property
    def scuffing_temperature_gradient_integral(self) -> 'float':
        """float: 'ScuffingTemperatureGradientIntegral' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingTemperatureGradientIntegral

        if temp is None:
            return None

        return temp

    @property
    def scuffing_temperature_method(self) -> '_1034.ScuffingTemperatureMethodsISO':
        """ScuffingTemperatureMethodsISO: 'ScuffingTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingTemperatureMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1034.ScuffingTemperatureMethodsISO)(value) if value is not None else None

    @property
    def single_stiffness(self) -> 'float':
        """float: 'SingleStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SingleStiffness

        if temp is None:
            return None

        return temp

    @property
    def stiffness_material_factor(self) -> 'float':
        """float: 'StiffnessMaterialFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessMaterialFactor

        if temp is None:
            return None

        return temp

    @property
    def test_torque(self) -> 'float':
        """float: 'TestTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TestTorque

        if temp is None:
            return None

        return temp

    @property
    def theoretical_single_stiffness(self) -> 'float':
        """float: 'TheoreticalSingleStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TheoreticalSingleStiffness

        if temp is None:
            return None

        return temp

    @property
    def thermo_elastic_factor_of_maximum_flash_temperature(self) -> 'float':
        """float: 'ThermoElasticFactorOfMaximumFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThermoElasticFactorOfMaximumFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def tip_relief(self) -> 'float':
        """float: 'TipRelief' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipRelief

        if temp is None:
            return None

        return temp

    @property
    def tip_relief_calculated(self) -> 'float':
        """float: 'TipReliefCalculated' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipReliefCalculated

        if temp is None:
            return None

        return temp

    @property
    def tip_relief_factor_integral(self) -> 'float':
        """float: 'TipReliefFactorIntegral' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipReliefFactorIntegral

        if temp is None:
            return None

        return temp

    @property
    def tip_relief_factor_for_micropitting(self) -> 'float':
        """float: 'TipReliefFactorForMicropitting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipReliefFactorForMicropitting

        if temp is None:
            return None

        return temp

    @property
    def tooth_stiffness_correction_factor(self) -> 'float':
        """float: 'ToothStiffnessCorrectionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothStiffnessCorrectionFactor

        if temp is None:
            return None

        return temp

    @property
    def transverse_base_pitch_deviation_factor_for_the_dynamic_load(self) -> 'float':
        """float: 'TransverseBasePitchDeviationFactorForTheDynamicLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseBasePitchDeviationFactorForTheDynamicLoad

        if temp is None:
            return None

        return temp

    @property
    def transverse_load_factor_contact(self) -> 'float':
        """float: 'TransverseLoadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseLoadFactorContact

        if temp is None:
            return None

        return temp

    @property
    def transverse_unit_load(self) -> 'float':
        """float: 'TransverseUnitLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseUnitLoad

        if temp is None:
            return None

        return temp

    @property
    def user_input_scuffing_integral_temperature_for_long_contact_times(self) -> 'float':
        """float: 'UserInputScuffingIntegralTemperatureForLongContactTimes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UserInputScuffingIntegralTemperatureForLongContactTimes

        if temp is None:
            return None

        return temp

    @property
    def user_input_scuffing_temperature(self) -> 'float':
        """float: 'UserInputScuffingTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UserInputScuffingTemperature

        if temp is None:
            return None

        return temp

    @property
    def user_input_scuffing_temperature_for_long_contact_times(self) -> 'float':
        """float: 'UserInputScuffingTemperatureForLongContactTimes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UserInputScuffingTemperatureForLongContactTimes

        if temp is None:
            return None

        return temp

    @property
    def single_flank_rating_of_test_gears_for_micropitting(self) -> '_481.ISO63362006MeshSingleFlankRating':
        """ISO63362006MeshSingleFlankRating: 'SingleFlankRatingOfTestGearsForMicropitting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SingleFlankRatingOfTestGearsForMicropitting

        if temp is None:
            return None

        if _481.ISO63362006MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast single_flank_rating_of_test_gears_for_micropitting to ISO63362006MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sorted_micro_pitting_results(self) -> '_428.CylindricalGearMicroPittingResults':
        """CylindricalGearMicroPittingResults: 'SortedMicroPittingResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SortedMicroPittingResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def isodin_cylindrical_gear_single_flank_ratings(self) -> 'List[_486.ISO6336AbstractMetalGearSingleFlankRating]':
        """List[ISO6336AbstractMetalGearSingleFlankRating]: 'ISODINCylindricalGearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISODINCylindricalGearSingleFlankRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
