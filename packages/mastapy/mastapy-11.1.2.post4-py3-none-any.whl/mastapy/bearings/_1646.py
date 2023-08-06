"""_1646.py

BearingSettings
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.bearings import (
    _1656, _1655, _1648, _1649
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.bearing_results.rolling.skf_module import _1854
from mastapy.utility import _1395
from mastapy._internal.python_net import python_net_import

_BEARING_SETTINGS = python_net_import('SMT.MastaAPI.Bearings', 'BearingSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingSettings',)


class BearingSettings(_1395.PerMachineSettings):
    """BearingSettings

    This is a mastapy class.
    """

    TYPE = _BEARING_SETTINGS

    def __init__(self, instance_to_wrap: 'BearingSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def ball_bearing_weibull_reliability_slope(self) -> 'float':
        """float: 'BallBearingWeibullReliabilitySlope' is the original name of this property."""

        temp = self.wrapped.BallBearingWeibullReliabilitySlope

        if temp is None:
            return None

        return temp

    @ball_bearing_weibull_reliability_slope.setter
    def ball_bearing_weibull_reliability_slope(self, value: 'float'):
        self.wrapped.BallBearingWeibullReliabilitySlope = float(value) if value else 0.0

    @property
    def default_roller_profile(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes':
        """enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes: 'DefaultRollerProfile' is the original name of this property."""

        temp = self.wrapped.DefaultRollerProfile

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @default_roller_profile.setter
    def default_roller_profile(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DefaultRollerProfile = value

    @property
    def enable_skf_module(self) -> 'bool':
        """bool: 'EnableSKFModule' is the original name of this property."""

        temp = self.wrapped.EnableSKFModule

        if temp is None:
            return None

        return temp

    @enable_skf_module.setter
    def enable_skf_module(self, value: 'bool'):
        self.wrapped.EnableSKFModule = bool(value) if value else False

    @property
    def failure_probability_for_rating_life_percent(self) -> '_1655.RatingLife':
        """RatingLife: 'FailureProbabilityForRatingLifePercent' is the original name of this property."""

        temp = self.wrapped.FailureProbabilityForRatingLifePercent

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1655.RatingLife)(value) if value is not None else None

    @failure_probability_for_rating_life_percent.setter
    def failure_probability_for_rating_life_percent(self, value: '_1655.RatingLife'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FailureProbabilityForRatingLifePercent = value

    @property
    def include_exponent_and_reduction_factors_in_isots162812008(self) -> '_1648.ExponentAndReductionFactorsInISO16281Calculation':
        """ExponentAndReductionFactorsInISO16281Calculation: 'IncludeExponentAndReductionFactorsInISOTS162812008' is the original name of this property."""

        temp = self.wrapped.IncludeExponentAndReductionFactorsInISOTS162812008

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1648.ExponentAndReductionFactorsInISO16281Calculation)(value) if value is not None else None

    @include_exponent_and_reduction_factors_in_isots162812008.setter
    def include_exponent_and_reduction_factors_in_isots162812008(self, value: '_1648.ExponentAndReductionFactorsInISO16281Calculation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeExponentAndReductionFactorsInISOTS162812008 = value

    @property
    def log_file_path(self) -> 'str':
        """str: 'LogFilePath' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LogFilePath

        if temp is None:
            return None

        return temp

    @property
    def log_http_requests(self) -> 'bool':
        """bool: 'LogHTTPRequests' is the original name of this property."""

        temp = self.wrapped.LogHTTPRequests

        if temp is None:
            return None

        return temp

    @log_http_requests.setter
    def log_http_requests(self, value: 'bool'):
        self.wrapped.LogHTTPRequests = bool(value) if value else False

    @property
    def lubricant_film_temperature_calculation_pressure_fed_grease_filled_bearings(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions':
        """enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions: 'LubricantFilmTemperatureCalculationPressureFedGreaseFilledBearings' is the original name of this property."""

        temp = self.wrapped.LubricantFilmTemperatureCalculationPressureFedGreaseFilledBearings

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @lubricant_film_temperature_calculation_pressure_fed_grease_filled_bearings.setter
    def lubricant_film_temperature_calculation_pressure_fed_grease_filled_bearings(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LubricantFilmTemperatureCalculationPressureFedGreaseFilledBearings = value

    @property
    def lubricant_film_temperature_calculation_splashed_submerged_bearings(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions':
        """enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions: 'LubricantFilmTemperatureCalculationSplashedSubmergedBearings' is the original name of this property."""

        temp = self.wrapped.LubricantFilmTemperatureCalculationSplashedSubmergedBearings

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @lubricant_film_temperature_calculation_splashed_submerged_bearings.setter
    def lubricant_film_temperature_calculation_splashed_submerged_bearings(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LubricantFilmTemperatureCalculationSplashedSubmergedBearings = value

    @property
    def roller_bearing_weibull_reliability_slope(self) -> 'float':
        """float: 'RollerBearingWeibullReliabilitySlope' is the original name of this property."""

        temp = self.wrapped.RollerBearingWeibullReliabilitySlope

        if temp is None:
            return None

        return temp

    @roller_bearing_weibull_reliability_slope.setter
    def roller_bearing_weibull_reliability_slope(self, value: 'float'):
        self.wrapped.RollerBearingWeibullReliabilitySlope = float(value) if value else 0.0

    @property
    def third_weibull_parameter(self) -> 'float':
        """float: 'ThirdWeibullParameter' is the original name of this property."""

        temp = self.wrapped.ThirdWeibullParameter

        if temp is None:
            return None

        return temp

    @third_weibull_parameter.setter
    def third_weibull_parameter(self, value: 'float'):
        self.wrapped.ThirdWeibullParameter = float(value) if value else 0.0

    @property
    def tolerance_used_for_diameter_warnings_and_database_filter(self) -> 'float':
        """float: 'ToleranceUsedForDiameterWarningsAndDatabaseFilter' is the original name of this property."""

        temp = self.wrapped.ToleranceUsedForDiameterWarningsAndDatabaseFilter

        if temp is None:
            return None

        return temp

    @tolerance_used_for_diameter_warnings_and_database_filter.setter
    def tolerance_used_for_diameter_warnings_and_database_filter(self, value: 'float'):
        self.wrapped.ToleranceUsedForDiameterWarningsAndDatabaseFilter = float(value) if value else 0.0

    @property
    def use_plain_journal_bearing_misalignment_factors(self) -> 'bool':
        """bool: 'UsePlainJournalBearingMisalignmentFactors' is the original name of this property."""

        temp = self.wrapped.UsePlainJournalBearingMisalignmentFactors

        if temp is None:
            return None

        return temp

    @use_plain_journal_bearing_misalignment_factors.setter
    def use_plain_journal_bearing_misalignment_factors(self, value: 'bool'):
        self.wrapped.UsePlainJournalBearingMisalignmentFactors = bool(value) if value else False

    @property
    def skf_authentication(self) -> '_1854.SKFAuthentication':
        """SKFAuthentication: 'SKFAuthentication' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SKFAuthentication

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
