"""_289.py

BevelHypoidGearRatingSettings
"""


from mastapy.gears.materials import _571
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.rating.iso_10300 import _392, _407, _400
from mastapy.gears.rating.hypoid import _413
from mastapy.utility import _1395
from mastapy._internal.python_net import python_net_import

_BEVEL_HYPOID_GEAR_RATING_SETTINGS = python_net_import('SMT.MastaAPI.Gears', 'BevelHypoidGearRatingSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelHypoidGearRatingSettings',)


class BevelHypoidGearRatingSettings(_1395.PerMachineSettings):
    """BevelHypoidGearRatingSettings

    This is a mastapy class.
    """

    TYPE = _BEVEL_HYPOID_GEAR_RATING_SETTINGS

    def __init__(self, instance_to_wrap: 'BevelHypoidGearRatingSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_rating_method(self) -> '_571.RatingMethods':
        """RatingMethods: 'BevelGearRatingMethod' is the original name of this property."""

        temp = self.wrapped.BevelGearRatingMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_571.RatingMethods)(value) if value is not None else None

    @bevel_gear_rating_method.setter
    def bevel_gear_rating_method(self, value: '_571.RatingMethods'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BevelGearRatingMethod = value

    @property
    def bevel_general_load_factors_k_method(self) -> '_392.GeneralLoadFactorCalculationMethod':
        """GeneralLoadFactorCalculationMethod: 'BevelGeneralLoadFactorsKMethod' is the original name of this property."""

        temp = self.wrapped.BevelGeneralLoadFactorsKMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_392.GeneralLoadFactorCalculationMethod)(value) if value is not None else None

    @bevel_general_load_factors_k_method.setter
    def bevel_general_load_factors_k_method(self, value: '_392.GeneralLoadFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BevelGeneralLoadFactorsKMethod = value

    @property
    def bevel_pitting_factor_calculation_method(self) -> '_407.PittingFactorCalculationMethod':
        """PittingFactorCalculationMethod: 'BevelPittingFactorCalculationMethod' is the original name of this property."""

        temp = self.wrapped.BevelPittingFactorCalculationMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_407.PittingFactorCalculationMethod)(value) if value is not None else None

    @bevel_pitting_factor_calculation_method.setter
    def bevel_pitting_factor_calculation_method(self, value: '_407.PittingFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BevelPittingFactorCalculationMethod = value

    @property
    def hypoid_gear_rating_method(self) -> '_413.HypoidRatingMethod':
        """HypoidRatingMethod: 'HypoidGearRatingMethod' is the original name of this property."""

        temp = self.wrapped.HypoidGearRatingMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_413.HypoidRatingMethod)(value) if value is not None else None

    @hypoid_gear_rating_method.setter
    def hypoid_gear_rating_method(self, value: '_413.HypoidRatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGearRatingMethod = value

    @property
    def hypoid_general_load_factors_k_method(self) -> '_392.GeneralLoadFactorCalculationMethod':
        """GeneralLoadFactorCalculationMethod: 'HypoidGeneralLoadFactorsKMethod' is the original name of this property."""

        temp = self.wrapped.HypoidGeneralLoadFactorsKMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_392.GeneralLoadFactorCalculationMethod)(value) if value is not None else None

    @hypoid_general_load_factors_k_method.setter
    def hypoid_general_load_factors_k_method(self, value: '_392.GeneralLoadFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGeneralLoadFactorsKMethod = value

    @property
    def hypoid_pitting_factor_calculation_method(self) -> '_407.PittingFactorCalculationMethod':
        """PittingFactorCalculationMethod: 'HypoidPittingFactorCalculationMethod' is the original name of this property."""

        temp = self.wrapped.HypoidPittingFactorCalculationMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_407.PittingFactorCalculationMethod)(value) if value is not None else None

    @hypoid_pitting_factor_calculation_method.setter
    def hypoid_pitting_factor_calculation_method(self, value: '_407.PittingFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidPittingFactorCalculationMethod = value

    @property
    def iso_rating_method_for_bevel_gears(self) -> '_400.ISO10300RatingMethod':
        """ISO10300RatingMethod: 'ISORatingMethodForBevelGears' is the original name of this property."""

        temp = self.wrapped.ISORatingMethodForBevelGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_400.ISO10300RatingMethod)(value) if value is not None else None

    @iso_rating_method_for_bevel_gears.setter
    def iso_rating_method_for_bevel_gears(self, value: '_400.ISO10300RatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ISORatingMethodForBevelGears = value

    @property
    def iso_rating_method_for_hypoid_gears(self) -> '_400.ISO10300RatingMethod':
        """ISO10300RatingMethod: 'ISORatingMethodForHypoidGears' is the original name of this property."""

        temp = self.wrapped.ISORatingMethodForHypoidGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_400.ISO10300RatingMethod)(value) if value is not None else None

    @iso_rating_method_for_hypoid_gears.setter
    def iso_rating_method_for_hypoid_gears(self, value: '_400.ISO10300RatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ISORatingMethodForHypoidGears = value

    @property
    def include_mesh_node_misalignments_in_default_report(self) -> 'bool':
        """bool: 'IncludeMeshNodeMisalignmentsInDefaultReport' is the original name of this property."""

        temp = self.wrapped.IncludeMeshNodeMisalignmentsInDefaultReport

        if temp is None:
            return None

        return temp

    @include_mesh_node_misalignments_in_default_report.setter
    def include_mesh_node_misalignments_in_default_report(self, value: 'bool'):
        self.wrapped.IncludeMeshNodeMisalignmentsInDefaultReport = bool(value) if value else False
