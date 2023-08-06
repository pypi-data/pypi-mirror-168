"""_431.py

CylindricalGearRatingSettings
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.rating.cylindrical import (
    _454, _440, _450, _441,
    _444, _447, _448, _449,
    _453
)
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.materials import _227
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.utility import _1395
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_RATING_SETTINGS = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearRatingSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearRatingSettings',)


class CylindricalGearRatingSettings(_1395.PerMachineSettings):
    """CylindricalGearRatingSettings

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_RATING_SETTINGS

    def __init__(self, instance_to_wrap: 'CylindricalGearRatingSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def agma_stress_cycle_factor_influence_factor(self) -> 'float':
        """float: 'AGMAStressCycleFactorInfluenceFactor' is the original name of this property."""

        temp = self.wrapped.AGMAStressCycleFactorInfluenceFactor

        if temp is None:
            return None

        return temp

    @agma_stress_cycle_factor_influence_factor.setter
    def agma_stress_cycle_factor_influence_factor(self, value: 'float'):
        self.wrapped.AGMAStressCycleFactorInfluenceFactor = float(value) if value else 0.0

    @property
    def allow_transverse_contact_ratio_less_than_one(self) -> 'bool':
        """bool: 'AllowTransverseContactRatioLessThanOne' is the original name of this property."""

        temp = self.wrapped.AllowTransverseContactRatioLessThanOne

        if temp is None:
            return None

        return temp

    @allow_transverse_contact_ratio_less_than_one.setter
    def allow_transverse_contact_ratio_less_than_one(self, value: 'bool'):
        self.wrapped.AllowTransverseContactRatioLessThanOne = bool(value) if value else False

    @property
    def always_use_chosen_tooth_thickness_for_bending_strength(self) -> 'bool':
        """bool: 'AlwaysUseChosenToothThicknessForBendingStrength' is the original name of this property."""

        temp = self.wrapped.AlwaysUseChosenToothThicknessForBendingStrength

        if temp is None:
            return None

        return temp

    @always_use_chosen_tooth_thickness_for_bending_strength.setter
    def always_use_chosen_tooth_thickness_for_bending_strength(self, value: 'bool'):
        self.wrapped.AlwaysUseChosenToothThicknessForBendingStrength = bool(value) if value else False

    @property
    def apply_application_and_dynamic_factor_by_default(self) -> 'bool':
        """bool: 'ApplyApplicationAndDynamicFactorByDefault' is the original name of this property."""

        temp = self.wrapped.ApplyApplicationAndDynamicFactorByDefault

        if temp is None:
            return None

        return temp

    @apply_application_and_dynamic_factor_by_default.setter
    def apply_application_and_dynamic_factor_by_default(self, value: 'bool'):
        self.wrapped.ApplyApplicationAndDynamicFactorByDefault = bool(value) if value else False

    @property
    def apply_work_hardening_factor_for_wrought_normalised_low_carbon_steel_and_cast_steel(self) -> 'bool':
        """bool: 'ApplyWorkHardeningFactorForWroughtNormalisedLowCarbonSteelAndCastSteel' is the original name of this property."""

        temp = self.wrapped.ApplyWorkHardeningFactorForWroughtNormalisedLowCarbonSteelAndCastSteel

        if temp is None:
            return None

        return temp

    @apply_work_hardening_factor_for_wrought_normalised_low_carbon_steel_and_cast_steel.setter
    def apply_work_hardening_factor_for_wrought_normalised_low_carbon_steel_and_cast_steel(self, value: 'bool'):
        self.wrapped.ApplyWorkHardeningFactorForWroughtNormalisedLowCarbonSteelAndCastSteel = bool(value) if value else False

    @property
    def chosen_tooth_thickness_for_bending_strength(self) -> '_454.ToothThicknesses':
        """ToothThicknesses: 'ChosenToothThicknessForBendingStrength' is the original name of this property."""

        temp = self.wrapped.ChosenToothThicknessForBendingStrength

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_454.ToothThicknesses)(value) if value is not None else None

    @chosen_tooth_thickness_for_bending_strength.setter
    def chosen_tooth_thickness_for_bending_strength(self, value: '_454.ToothThicknesses'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ChosenToothThicknessForBendingStrength = value

    @property
    def dynamic_factor_method(self) -> '_440.DynamicFactorMethods':
        """DynamicFactorMethods: 'DynamicFactorMethod' is the original name of this property."""

        temp = self.wrapped.DynamicFactorMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_440.DynamicFactorMethods)(value) if value is not None else None

    @dynamic_factor_method.setter
    def dynamic_factor_method(self, value: '_440.DynamicFactorMethods'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DynamicFactorMethod = value

    @property
    def film_thickness_equation_for_scuffing(self) -> '_450.ScuffingMethods':
        """ScuffingMethods: 'FilmThicknessEquationForScuffing' is the original name of this property."""

        temp = self.wrapped.FilmThicknessEquationForScuffing

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_450.ScuffingMethods)(value) if value is not None else None

    @film_thickness_equation_for_scuffing.setter
    def film_thickness_equation_for_scuffing(self, value: '_450.ScuffingMethods'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FilmThicknessEquationForScuffing = value

    @property
    def gear_blank_factor_calculation_option(self) -> '_441.GearBlankFactorCalculationOptions':
        """GearBlankFactorCalculationOptions: 'GearBlankFactorCalculationOption' is the original name of this property."""

        temp = self.wrapped.GearBlankFactorCalculationOption

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_441.GearBlankFactorCalculationOptions)(value) if value is not None else None

    @gear_blank_factor_calculation_option.setter
    def gear_blank_factor_calculation_option(self, value: '_441.GearBlankFactorCalculationOptions'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearBlankFactorCalculationOption = value

    @property
    def include_rim_thickness_factor(self) -> 'bool':
        """bool: 'IncludeRimThicknessFactor' is the original name of this property."""

        temp = self.wrapped.IncludeRimThicknessFactor

        if temp is None:
            return None

        return temp

    @include_rim_thickness_factor.setter
    def include_rim_thickness_factor(self, value: 'bool'):
        self.wrapped.IncludeRimThicknessFactor = bool(value) if value else False

    @property
    def internal_gear_root_fillet_radius_is_always_equal_to_basic_rack_root_fillet_radius(self) -> 'bool':
        """bool: 'InternalGearRootFilletRadiusIsAlwaysEqualToBasicRackRootFilletRadius' is the original name of this property."""

        temp = self.wrapped.InternalGearRootFilletRadiusIsAlwaysEqualToBasicRackRootFilletRadius

        if temp is None:
            return None

        return temp

    @internal_gear_root_fillet_radius_is_always_equal_to_basic_rack_root_fillet_radius.setter
    def internal_gear_root_fillet_radius_is_always_equal_to_basic_rack_root_fillet_radius(self, value: 'bool'):
        self.wrapped.InternalGearRootFilletRadiusIsAlwaysEqualToBasicRackRootFilletRadius = bool(value) if value else False

    @property
    def limit_dynamic_factor_if_not_in_main_resonance_range_by_default(self) -> 'bool':
        """bool: 'LimitDynamicFactorIfNotInMainResonanceRangeByDefault' is the original name of this property."""

        temp = self.wrapped.LimitDynamicFactorIfNotInMainResonanceRangeByDefault

        if temp is None:
            return None

        return temp

    @limit_dynamic_factor_if_not_in_main_resonance_range_by_default.setter
    def limit_dynamic_factor_if_not_in_main_resonance_range_by_default(self, value: 'bool'):
        self.wrapped.LimitDynamicFactorIfNotInMainResonanceRangeByDefault = bool(value) if value else False

    @property
    def limit_micro_geometry_factor_for_the_dynamic_load_by_default(self) -> 'bool':
        """bool: 'LimitMicroGeometryFactorForTheDynamicLoadByDefault' is the original name of this property."""

        temp = self.wrapped.LimitMicroGeometryFactorForTheDynamicLoadByDefault

        if temp is None:
            return None

        return temp

    @limit_micro_geometry_factor_for_the_dynamic_load_by_default.setter
    def limit_micro_geometry_factor_for_the_dynamic_load_by_default(self, value: 'bool'):
        self.wrapped.LimitMicroGeometryFactorForTheDynamicLoadByDefault = bool(value) if value else False

    @property
    def mean_coefficient_of_friction_flash_temperature_method(self) -> 'float':
        """float: 'MeanCoefficientOfFrictionFlashTemperatureMethod' is the original name of this property."""

        temp = self.wrapped.MeanCoefficientOfFrictionFlashTemperatureMethod

        if temp is None:
            return None

        return temp

    @mean_coefficient_of_friction_flash_temperature_method.setter
    def mean_coefficient_of_friction_flash_temperature_method(self, value: 'float'):
        self.wrapped.MeanCoefficientOfFrictionFlashTemperatureMethod = float(value) if value else 0.0

    @property
    def micropitting_rating_method(self) -> '_444.MicropittingRatingMethod':
        """MicropittingRatingMethod: 'MicropittingRatingMethod' is the original name of this property."""

        temp = self.wrapped.MicropittingRatingMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_444.MicropittingRatingMethod)(value) if value is not None else None

    @micropitting_rating_method.setter
    def micropitting_rating_method(self, value: '_444.MicropittingRatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MicropittingRatingMethod = value

    @property
    def number_of_load_strips_for_basic_ltca(self) -> 'int':
        """int: 'NumberOfLoadStripsForBasicLTCA' is the original name of this property."""

        temp = self.wrapped.NumberOfLoadStripsForBasicLTCA

        if temp is None:
            return None

        return temp

    @number_of_load_strips_for_basic_ltca.setter
    def number_of_load_strips_for_basic_ltca(self, value: 'int'):
        self.wrapped.NumberOfLoadStripsForBasicLTCA = int(value) if value else 0

    @property
    def number_of_points_along_profile_for_micropitting_calculation(self) -> 'int':
        """int: 'NumberOfPointsAlongProfileForMicropittingCalculation' is the original name of this property."""

        temp = self.wrapped.NumberOfPointsAlongProfileForMicropittingCalculation

        if temp is None:
            return None

        return temp

    @number_of_points_along_profile_for_micropitting_calculation.setter
    def number_of_points_along_profile_for_micropitting_calculation(self, value: 'int'):
        self.wrapped.NumberOfPointsAlongProfileForMicropittingCalculation = int(value) if value else 0

    @property
    def number_of_points_along_profile_for_scuffing_calculation(self) -> 'int':
        """int: 'NumberOfPointsAlongProfileForScuffingCalculation' is the original name of this property."""

        temp = self.wrapped.NumberOfPointsAlongProfileForScuffingCalculation

        if temp is None:
            return None

        return temp

    @number_of_points_along_profile_for_scuffing_calculation.setter
    def number_of_points_along_profile_for_scuffing_calculation(self, value: 'int'):
        self.wrapped.NumberOfPointsAlongProfileForScuffingCalculation = int(value) if value else 0

    @property
    def number_of_points_along_profile_for_tooth_flank_fracture_calculation(self) -> 'int':
        """int: 'NumberOfPointsAlongProfileForToothFlankFractureCalculation' is the original name of this property."""

        temp = self.wrapped.NumberOfPointsAlongProfileForToothFlankFractureCalculation

        if temp is None:
            return None

        return temp

    @number_of_points_along_profile_for_tooth_flank_fracture_calculation.setter
    def number_of_points_along_profile_for_tooth_flank_fracture_calculation(self, value: 'int'):
        self.wrapped.NumberOfPointsAlongProfileForToothFlankFractureCalculation = int(value) if value else 0

    @property
    def number_of_rotations_for_basic_ltca(self) -> 'int':
        """int: 'NumberOfRotationsForBasicLTCA' is the original name of this property."""

        temp = self.wrapped.NumberOfRotationsForBasicLTCA

        if temp is None:
            return None

        return temp

    @number_of_rotations_for_basic_ltca.setter
    def number_of_rotations_for_basic_ltca(self, value: 'int'):
        self.wrapped.NumberOfRotationsForBasicLTCA = int(value) if value else 0

    @property
    def permissible_bending_stress_method(self) -> '_447.RatingMethod':
        """RatingMethod: 'PermissibleBendingStressMethod' is the original name of this property."""

        temp = self.wrapped.PermissibleBendingStressMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_447.RatingMethod)(value) if value is not None else None

    @permissible_bending_stress_method.setter
    def permissible_bending_stress_method(self, value: '_447.RatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PermissibleBendingStressMethod = value

    @property
    def rating_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_CylindricalGearRatingMethods':
        """enum_with_selected_value.EnumWithSelectedValue_CylindricalGearRatingMethods: 'RatingMethod' is the original name of this property."""

        temp = self.wrapped.RatingMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CylindricalGearRatingMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @rating_method.setter
    def rating_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_CylindricalGearRatingMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CylindricalGearRatingMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.RatingMethod = value

    @property
    def scuffing_rating_method_flash_temperature_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod':
        """enum_with_selected_value.EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod: 'ScuffingRatingMethodFlashTemperatureMethod' is the original name of this property."""

        temp = self.wrapped.ScuffingRatingMethodFlashTemperatureMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @scuffing_rating_method_flash_temperature_method.setter
    def scuffing_rating_method_flash_temperature_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ScuffingRatingMethodFlashTemperatureMethod = value

    @property
    def scuffing_rating_method_integral_temperature_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod':
        """enum_with_selected_value.EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod: 'ScuffingRatingMethodIntegralTemperatureMethod' is the original name of this property."""

        temp = self.wrapped.ScuffingRatingMethodIntegralTemperatureMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @scuffing_rating_method_integral_temperature_method.setter
    def scuffing_rating_method_integral_temperature_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ScuffingRatingMethodIntegralTemperatureMethod = value

    @property
    def show_rating_settings_in_report(self) -> 'bool':
        """bool: 'ShowRatingSettingsInReport' is the original name of this property."""

        temp = self.wrapped.ShowRatingSettingsInReport

        if temp is None:
            return None

        return temp

    @show_rating_settings_in_report.setter
    def show_rating_settings_in_report(self, value: 'bool'):
        self.wrapped.ShowRatingSettingsInReport = bool(value) if value else False

    @property
    def show_vdi_rating_when_available(self) -> 'bool':
        """bool: 'ShowVDIRatingWhenAvailable' is the original name of this property."""

        temp = self.wrapped.ShowVDIRatingWhenAvailable

        if temp is None:
            return None

        return temp

    @show_vdi_rating_when_available.setter
    def show_vdi_rating_when_available(self, value: 'bool'):
        self.wrapped.ShowVDIRatingWhenAvailable = bool(value) if value else False

    @property
    def tip_relief_in_scuffing_calculation(self) -> '_453.TipReliefScuffingOptions':
        """TipReliefScuffingOptions: 'TipReliefInScuffingCalculation' is the original name of this property."""

        temp = self.wrapped.TipReliefInScuffingCalculation

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_453.TipReliefScuffingOptions)(value) if value is not None else None

    @tip_relief_in_scuffing_calculation.setter
    def tip_relief_in_scuffing_calculation(self, value: '_453.TipReliefScuffingOptions'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TipReliefInScuffingCalculation = value

    @property
    def use_10_for_contact_ratio_factor_contact_for_spur_gears_with_contact_ratio_less_than_20(self) -> 'bool':
        """bool: 'Use10ForContactRatioFactorContactForSpurGearsWithContactRatioLessThan20' is the original name of this property."""

        temp = self.wrapped.Use10ForContactRatioFactorContactForSpurGearsWithContactRatioLessThan20

        if temp is None:
            return None

        return temp

    @use_10_for_contact_ratio_factor_contact_for_spur_gears_with_contact_ratio_less_than_20.setter
    def use_10_for_contact_ratio_factor_contact_for_spur_gears_with_contact_ratio_less_than_20(self, value: 'bool'):
        self.wrapped.Use10ForContactRatioFactorContactForSpurGearsWithContactRatioLessThan20 = bool(value) if value else False

    @property
    def use_interpolated_single_pair_tooth_contact_factor_for_hcr_helical_gears(self) -> 'bool':
        """bool: 'UseInterpolatedSinglePairToothContactFactorForHCRHelicalGears' is the original name of this property."""

        temp = self.wrapped.UseInterpolatedSinglePairToothContactFactorForHCRHelicalGears

        if temp is None:
            return None

        return temp

    @use_interpolated_single_pair_tooth_contact_factor_for_hcr_helical_gears.setter
    def use_interpolated_single_pair_tooth_contact_factor_for_hcr_helical_gears(self, value: 'bool'):
        self.wrapped.UseInterpolatedSinglePairToothContactFactorForHCRHelicalGears = bool(value) if value else False

    @property
    def use_ltca_stresses_in_gear_rating(self) -> 'bool':
        """bool: 'UseLTCAStressesInGearRating' is the original name of this property."""

        temp = self.wrapped.UseLTCAStressesInGearRating

        if temp is None:
            return None

        return temp

    @use_ltca_stresses_in_gear_rating.setter
    def use_ltca_stresses_in_gear_rating(self, value: 'bool'):
        self.wrapped.UseLTCAStressesInGearRating = bool(value) if value else False

    @property
    def use_point_of_highest_stress_to_calculate_face_load_factor(self) -> 'bool':
        """bool: 'UsePointOfHighestStressToCalculateFaceLoadFactor' is the original name of this property."""

        temp = self.wrapped.UsePointOfHighestStressToCalculateFaceLoadFactor

        if temp is None:
            return None

        return temp

    @use_point_of_highest_stress_to_calculate_face_load_factor.setter
    def use_point_of_highest_stress_to_calculate_face_load_factor(self, value: 'bool'):
        self.wrapped.UsePointOfHighestStressToCalculateFaceLoadFactor = bool(value) if value else False

    @property
    def vdi_rating_geometry_calculation_method(self) -> 'overridable.Overridable_CylindricalGearRatingMethods':
        """overridable.Overridable_CylindricalGearRatingMethods: 'VDIRatingGeometryCalculationMethod' is the original name of this property."""

        temp = self.wrapped.VDIRatingGeometryCalculationMethod

        if temp is None:
            return None

        value = overridable.Overridable_CylindricalGearRatingMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @vdi_rating_geometry_calculation_method.setter
    def vdi_rating_geometry_calculation_method(self, value: 'overridable.Overridable_CylindricalGearRatingMethods.implicit_type()'):
        wrapper_type = overridable.Overridable_CylindricalGearRatingMethods.wrapper_type()
        enclosed_type = overridable.Overridable_CylindricalGearRatingMethods.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.VDIRatingGeometryCalculationMethod = value
