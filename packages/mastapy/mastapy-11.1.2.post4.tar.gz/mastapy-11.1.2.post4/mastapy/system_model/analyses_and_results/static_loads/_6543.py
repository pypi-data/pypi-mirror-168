"""_6543.py

BearingLoadCase
"""


from typing import List

from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_results.rolling import _1734, _1828, _1829
from mastapy.system_model.analyses_and_results.mbd_analyses import _5121
from mastapy.materials.efficiency import _266
from mastapy.math_utility.hertzian_contact import _1378
from mastapy.utility import _1393
from mastapy.bearings.bearing_results import _1706
from mastapy.system_model.part_model import _2191
from mastapy.math_utility.measured_vectors import _1371
from mastapy.bearings.tolerances import _1678, _1684
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.analyses_and_results.static_loads import _6573

_ARRAY = python_net_import('System', 'Array')
_BEARING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BearingLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingLoadCase',)


class BearingLoadCase(_6573.ConnectorLoadCase):
    """BearingLoadCase

    This is a mastapy class.
    """

    TYPE = _BEARING_LOAD_CASE

    def __init__(self, instance_to_wrap: 'BearingLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_displacement_preload(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'AxialDisplacementPreload' is the original name of this property."""

        temp = self.wrapped.AxialDisplacementPreload

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @axial_displacement_preload.setter
    def axial_displacement_preload(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.AxialDisplacementPreload = value

    @property
    def axial_force_preload(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'AxialForcePreload' is the original name of this property."""

        temp = self.wrapped.AxialForcePreload

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @axial_force_preload.setter
    def axial_force_preload(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.AxialForcePreload = value

    @property
    def axial_internal_clearance(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'AxialInternalClearance' is the original name of this property."""

        temp = self.wrapped.AxialInternalClearance

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @axial_internal_clearance.setter
    def axial_internal_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.AxialInternalClearance = value

    @property
    def axial_internal_clearance_tolerance_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'AxialInternalClearanceToleranceFactor' is the original name of this property."""

        temp = self.wrapped.AxialInternalClearanceToleranceFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @axial_internal_clearance_tolerance_factor.setter
    def axial_internal_clearance_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.AxialInternalClearanceToleranceFactor = value

    @property
    def ball_bearing_friction_model_for_gyroscopic_moment(self) -> 'overridable.Overridable_FrictionModelForGyroscopicMoment':
        """overridable.Overridable_FrictionModelForGyroscopicMoment: 'BallBearingFrictionModelForGyroscopicMoment' is the original name of this property."""

        temp = self.wrapped.BallBearingFrictionModelForGyroscopicMoment

        if temp is None:
            return None

        value = overridable.Overridable_FrictionModelForGyroscopicMoment.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @ball_bearing_friction_model_for_gyroscopic_moment.setter
    def ball_bearing_friction_model_for_gyroscopic_moment(self, value: 'overridable.Overridable_FrictionModelForGyroscopicMoment.implicit_type()'):
        wrapper_type = overridable.Overridable_FrictionModelForGyroscopicMoment.wrapper_type()
        enclosed_type = overridable.Overridable_FrictionModelForGyroscopicMoment.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.BallBearingFrictionModelForGyroscopicMoment = value

    @property
    def bearing_life_adjustment_factor_for_operating_conditions(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'BearingLifeAdjustmentFactorForOperatingConditions' is the original name of this property."""

        temp = self.wrapped.BearingLifeAdjustmentFactorForOperatingConditions

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @bearing_life_adjustment_factor_for_operating_conditions.setter
    def bearing_life_adjustment_factor_for_operating_conditions(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.BearingLifeAdjustmentFactorForOperatingConditions = value

    @property
    def bearing_life_adjustment_factor_for_special_bearing_properties(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'BearingLifeAdjustmentFactorForSpecialBearingProperties' is the original name of this property."""

        temp = self.wrapped.BearingLifeAdjustmentFactorForSpecialBearingProperties

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @bearing_life_adjustment_factor_for_special_bearing_properties.setter
    def bearing_life_adjustment_factor_for_special_bearing_properties(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.BearingLifeAdjustmentFactorForSpecialBearingProperties = value

    @property
    def bearing_life_modification_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'BearingLifeModificationFactor' is the original name of this property."""

        temp = self.wrapped.BearingLifeModificationFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @bearing_life_modification_factor.setter
    def bearing_life_modification_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.BearingLifeModificationFactor = value

    @property
    def bearing_stiffness_model(self) -> '_5121.BearingStiffnessModel':
        """BearingStiffnessModel: 'BearingStiffnessModel' is the original name of this property."""

        temp = self.wrapped.BearingStiffnessModel

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5121.BearingStiffnessModel)(value) if value is not None else None

    @bearing_stiffness_model.setter
    def bearing_stiffness_model(self, value: '_5121.BearingStiffnessModel'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BearingStiffnessModel = value

    @property
    def bearing_stiffness_model_used_in_analysis(self) -> '_5121.BearingStiffnessModel':
        """BearingStiffnessModel: 'BearingStiffnessModelUsedInAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingStiffnessModelUsedInAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5121.BearingStiffnessModel)(value) if value is not None else None

    @property
    def coefficient_of_friction(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'CoefficientOfFriction' is the original name of this property."""

        temp = self.wrapped.CoefficientOfFriction

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @coefficient_of_friction.setter
    def coefficient_of_friction(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.CoefficientOfFriction = value

    @property
    def contact_angle(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ContactAngle' is the original name of this property."""

        temp = self.wrapped.ContactAngle

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @contact_angle.setter
    def contact_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ContactAngle = value

    @property
    def contact_stiffness(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ContactStiffness' is the original name of this property."""

        temp = self.wrapped.ContactStiffness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @contact_stiffness.setter
    def contact_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ContactStiffness = value

    @property
    def efficiency_rating_method(self) -> 'overridable.Overridable_BearingEfficiencyRatingMethod':
        """overridable.Overridable_BearingEfficiencyRatingMethod: 'EfficiencyRatingMethod' is the original name of this property."""

        temp = self.wrapped.EfficiencyRatingMethod

        if temp is None:
            return None

        value = overridable.Overridable_BearingEfficiencyRatingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @efficiency_rating_method.setter
    def efficiency_rating_method(self, value: 'overridable.Overridable_BearingEfficiencyRatingMethod.implicit_type()'):
        wrapper_type = overridable.Overridable_BearingEfficiencyRatingMethod.wrapper_type()
        enclosed_type = overridable.Overridable_BearingEfficiencyRatingMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.EfficiencyRatingMethod = value

    @property
    def element_temperature(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ElementTemperature' is the original name of this property."""

        temp = self.wrapped.ElementTemperature

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @element_temperature.setter
    def element_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ElementTemperature = value

    @property
    def first_element_angle(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FirstElementAngle' is the original name of this property."""

        temp = self.wrapped.FirstElementAngle

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @first_element_angle.setter
    def first_element_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FirstElementAngle = value

    @property
    def grid_refinement_factor_contact_width(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'GridRefinementFactorContactWidth' is the original name of this property."""

        temp = self.wrapped.GridRefinementFactorContactWidth

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @grid_refinement_factor_contact_width.setter
    def grid_refinement_factor_contact_width(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.GridRefinementFactorContactWidth = value

    @property
    def grid_refinement_factor_rib_height(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'GridRefinementFactorRibHeight' is the original name of this property."""

        temp = self.wrapped.GridRefinementFactorRibHeight

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @grid_refinement_factor_rib_height.setter
    def grid_refinement_factor_rib_height(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.GridRefinementFactorRibHeight = value

    @property
    def hertzian_contact_deflection_calculation_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod':
        """enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod: 'HertzianContactDeflectionCalculationMethod' is the original name of this property."""

        temp = self.wrapped.HertzianContactDeflectionCalculationMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @hertzian_contact_deflection_calculation_method.setter
    def hertzian_contact_deflection_calculation_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.HertzianContactDeflectionCalculationMethod = value

    @property
    def include_fitting_effects(self) -> '_1393.LoadCaseOverrideOption':
        """LoadCaseOverrideOption: 'IncludeFittingEffects' is the original name of this property."""

        temp = self.wrapped.IncludeFittingEffects

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1393.LoadCaseOverrideOption)(value) if value is not None else None

    @include_fitting_effects.setter
    def include_fitting_effects(self, value: '_1393.LoadCaseOverrideOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeFittingEffects = value

    @property
    def include_rib_contact_analysis(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'IncludeRibContactAnalysis' is the original name of this property."""

        temp = self.wrapped.IncludeRibContactAnalysis

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @include_rib_contact_analysis.setter
    def include_rib_contact_analysis(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.IncludeRibContactAnalysis = value

    @property
    def include_ring_ovality(self) -> '_1393.LoadCaseOverrideOption':
        """LoadCaseOverrideOption: 'IncludeRingOvality' is the original name of this property."""

        temp = self.wrapped.IncludeRingOvality

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1393.LoadCaseOverrideOption)(value) if value is not None else None

    @include_ring_ovality.setter
    def include_ring_ovality(self, value: '_1393.LoadCaseOverrideOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeRingOvality = value

    @property
    def include_thermal_expansion_effects(self) -> '_1393.LoadCaseOverrideOption':
        """LoadCaseOverrideOption: 'IncludeThermalExpansionEffects' is the original name of this property."""

        temp = self.wrapped.IncludeThermalExpansionEffects

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1393.LoadCaseOverrideOption)(value) if value is not None else None

    @include_thermal_expansion_effects.setter
    def include_thermal_expansion_effects(self, value: '_1393.LoadCaseOverrideOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeThermalExpansionEffects = value

    @property
    def inner_mounting_sleeve_bore_tolerance_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'InnerMountingSleeveBoreToleranceFactor' is the original name of this property."""

        temp = self.wrapped.InnerMountingSleeveBoreToleranceFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @inner_mounting_sleeve_bore_tolerance_factor.setter
    def inner_mounting_sleeve_bore_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.InnerMountingSleeveBoreToleranceFactor = value

    @property
    def inner_mounting_sleeve_outer_diameter_tolerance_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'InnerMountingSleeveOuterDiameterToleranceFactor' is the original name of this property."""

        temp = self.wrapped.InnerMountingSleeveOuterDiameterToleranceFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @inner_mounting_sleeve_outer_diameter_tolerance_factor.setter
    def inner_mounting_sleeve_outer_diameter_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.InnerMountingSleeveOuterDiameterToleranceFactor = value

    @property
    def inner_mounting_sleeve_temperature(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'InnerMountingSleeveTemperature' is the original name of this property."""

        temp = self.wrapped.InnerMountingSleeveTemperature

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @inner_mounting_sleeve_temperature.setter
    def inner_mounting_sleeve_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.InnerMountingSleeveTemperature = value

    @property
    def inner_node_meaning(self) -> 'str':
        """str: 'InnerNodeMeaning' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerNodeMeaning

        if temp is None:
            return None

        return temp

    @property
    def lubricant_film_temperature(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'LubricantFilmTemperature' is the original name of this property."""

        temp = self.wrapped.LubricantFilmTemperature

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @lubricant_film_temperature.setter
    def lubricant_film_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.LubricantFilmTemperature = value

    @property
    def lubricant_windage_churning_temperature(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'LubricantWindageChurningTemperature' is the original name of this property."""

        temp = self.wrapped.LubricantWindageChurningTemperature

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @lubricant_windage_churning_temperature.setter
    def lubricant_windage_churning_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.LubricantWindageChurningTemperature = value

    @property
    def minimum_clearance_for_ribs(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumClearanceForRibs' is the original name of this property."""

        temp = self.wrapped.MinimumClearanceForRibs

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minimum_clearance_for_ribs.setter
    def minimum_clearance_for_ribs(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumClearanceForRibs = value

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumForceForBearingToBeConsideredLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumForceForBearingToBeConsideredLoaded

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    def minimum_force_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumForceForBearingToBeConsideredLoaded = value

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumMomentForBearingToBeConsideredLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumMomentForBearingToBeConsideredLoaded

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    def minimum_moment_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumMomentForBearingToBeConsideredLoaded = value

    @property
    def model_bearing_mounting_clearances_automatically(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'ModelBearingMountingClearancesAutomatically' is the original name of this property."""

        temp = self.wrapped.ModelBearingMountingClearancesAutomatically

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @model_bearing_mounting_clearances_automatically.setter
    def model_bearing_mounting_clearances_automatically(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.ModelBearingMountingClearancesAutomatically = value

    @property
    def number_of_grid_points_across_rib_contact_width(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfGridPointsAcrossRibContactWidth' is the original name of this property."""

        temp = self.wrapped.NumberOfGridPointsAcrossRibContactWidth

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_grid_points_across_rib_contact_width.setter
    def number_of_grid_points_across_rib_contact_width(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfGridPointsAcrossRibContactWidth = value

    @property
    def number_of_grid_points_across_rib_height(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfGridPointsAcrossRibHeight' is the original name of this property."""

        temp = self.wrapped.NumberOfGridPointsAcrossRibHeight

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_grid_points_across_rib_height.setter
    def number_of_grid_points_across_rib_height(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfGridPointsAcrossRibHeight = value

    @property
    def number_of_strips_for_roller_calculation(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfStripsForRollerCalculation' is the original name of this property."""

        temp = self.wrapped.NumberOfStripsForRollerCalculation

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_strips_for_roller_calculation.setter
    def number_of_strips_for_roller_calculation(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfStripsForRollerCalculation = value

    @property
    def oil_dip_coefficient(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OilDipCoefficient' is the original name of this property."""

        temp = self.wrapped.OilDipCoefficient

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @oil_dip_coefficient.setter
    def oil_dip_coefficient(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.OilDipCoefficient = value

    @property
    def oil_inlet_temperature(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OilInletTemperature' is the original name of this property."""

        temp = self.wrapped.OilInletTemperature

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @oil_inlet_temperature.setter
    def oil_inlet_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.OilInletTemperature = value

    @property
    def oil_level(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OilLevel' is the original name of this property."""

        temp = self.wrapped.OilLevel

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @oil_level.setter
    def oil_level(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.OilLevel = value

    @property
    def outer_mounting_sleeve_bore_tolerance_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OuterMountingSleeveBoreToleranceFactor' is the original name of this property."""

        temp = self.wrapped.OuterMountingSleeveBoreToleranceFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @outer_mounting_sleeve_bore_tolerance_factor.setter
    def outer_mounting_sleeve_bore_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.OuterMountingSleeveBoreToleranceFactor = value

    @property
    def outer_mounting_sleeve_outer_diameter_tolerance_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OuterMountingSleeveOuterDiameterToleranceFactor' is the original name of this property."""

        temp = self.wrapped.OuterMountingSleeveOuterDiameterToleranceFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @outer_mounting_sleeve_outer_diameter_tolerance_factor.setter
    def outer_mounting_sleeve_outer_diameter_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.OuterMountingSleeveOuterDiameterToleranceFactor = value

    @property
    def outer_mounting_sleeve_temperature(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OuterMountingSleeveTemperature' is the original name of this property."""

        temp = self.wrapped.OuterMountingSleeveTemperature

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @outer_mounting_sleeve_temperature.setter
    def outer_mounting_sleeve_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.OuterMountingSleeveTemperature = value

    @property
    def outer_node_meaning(self) -> 'str':
        """str: 'OuterNodeMeaning' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterNodeMeaning

        if temp is None:
            return None

        return temp

    @property
    def override_all_planets_inner_support_detail(self) -> 'bool':
        """bool: 'OverrideAllPlanetsInnerSupportDetail' is the original name of this property."""

        temp = self.wrapped.OverrideAllPlanetsInnerSupportDetail

        if temp is None:
            return None

        return temp

    @override_all_planets_inner_support_detail.setter
    def override_all_planets_inner_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsInnerSupportDetail = bool(value) if value else False

    @property
    def override_all_planets_left_support_detail(self) -> 'bool':
        """bool: 'OverrideAllPlanetsLeftSupportDetail' is the original name of this property."""

        temp = self.wrapped.OverrideAllPlanetsLeftSupportDetail

        if temp is None:
            return None

        return temp

    @override_all_planets_left_support_detail.setter
    def override_all_planets_left_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsLeftSupportDetail = bool(value) if value else False

    @property
    def override_all_planets_outer_support_detail(self) -> 'bool':
        """bool: 'OverrideAllPlanetsOuterSupportDetail' is the original name of this property."""

        temp = self.wrapped.OverrideAllPlanetsOuterSupportDetail

        if temp is None:
            return None

        return temp

    @override_all_planets_outer_support_detail.setter
    def override_all_planets_outer_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsOuterSupportDetail = bool(value) if value else False

    @property
    def override_all_planets_right_support_detail(self) -> 'bool':
        """bool: 'OverrideAllPlanetsRightSupportDetail' is the original name of this property."""

        temp = self.wrapped.OverrideAllPlanetsRightSupportDetail

        if temp is None:
            return None

        return temp

    @override_all_planets_right_support_detail.setter
    def override_all_planets_right_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsRightSupportDetail = bool(value) if value else False

    @property
    def override_design_inner_support_detail(self) -> 'bool':
        """bool: 'OverrideDesignInnerSupportDetail' is the original name of this property."""

        temp = self.wrapped.OverrideDesignInnerSupportDetail

        if temp is None:
            return None

        return temp

    @override_design_inner_support_detail.setter
    def override_design_inner_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignInnerSupportDetail = bool(value) if value else False

    @property
    def override_design_left_support_detail(self) -> 'bool':
        """bool: 'OverrideDesignLeftSupportDetail' is the original name of this property."""

        temp = self.wrapped.OverrideDesignLeftSupportDetail

        if temp is None:
            return None

        return temp

    @override_design_left_support_detail.setter
    def override_design_left_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignLeftSupportDetail = bool(value) if value else False

    @property
    def override_design_outer_support_detail(self) -> 'bool':
        """bool: 'OverrideDesignOuterSupportDetail' is the original name of this property."""

        temp = self.wrapped.OverrideDesignOuterSupportDetail

        if temp is None:
            return None

        return temp

    @override_design_outer_support_detail.setter
    def override_design_outer_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignOuterSupportDetail = bool(value) if value else False

    @property
    def override_design_right_support_detail(self) -> 'bool':
        """bool: 'OverrideDesignRightSupportDetail' is the original name of this property."""

        temp = self.wrapped.OverrideDesignRightSupportDetail

        if temp is None:
            return None

        return temp

    @override_design_right_support_detail.setter
    def override_design_right_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignRightSupportDetail = bool(value) if value else False

    @property
    def override_design_specified_stiffness_matrix(self) -> 'bool':
        """bool: 'OverrideDesignSpecifiedStiffnessMatrix' is the original name of this property."""

        temp = self.wrapped.OverrideDesignSpecifiedStiffnessMatrix

        if temp is None:
            return None

        return temp

    @override_design_specified_stiffness_matrix.setter
    def override_design_specified_stiffness_matrix(self, value: 'bool'):
        self.wrapped.OverrideDesignSpecifiedStiffnessMatrix = bool(value) if value else False

    @property
    def permissible_axial_load_calculation_method(self) -> 'overridable.Overridable_CylindricalRollerMaxAxialLoadMethod':
        """overridable.Overridable_CylindricalRollerMaxAxialLoadMethod: 'PermissibleAxialLoadCalculationMethod' is the original name of this property."""

        temp = self.wrapped.PermissibleAxialLoadCalculationMethod

        if temp is None:
            return None

        value = overridable.Overridable_CylindricalRollerMaxAxialLoadMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @permissible_axial_load_calculation_method.setter
    def permissible_axial_load_calculation_method(self, value: 'overridable.Overridable_CylindricalRollerMaxAxialLoadMethod.implicit_type()'):
        wrapper_type = overridable.Overridable_CylindricalRollerMaxAxialLoadMethod.wrapper_type()
        enclosed_type = overridable.Overridable_CylindricalRollerMaxAxialLoadMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.PermissibleAxialLoadCalculationMethod = value

    @property
    def preload_spring_initial_compression(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PreloadSpringInitialCompression' is the original name of this property."""

        temp = self.wrapped.PreloadSpringInitialCompression

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @preload_spring_initial_compression.setter
    def preload_spring_initial_compression(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PreloadSpringInitialCompression = value

    @property
    def radial_internal_clearance(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RadialInternalClearance' is the original name of this property."""

        temp = self.wrapped.RadialInternalClearance

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @radial_internal_clearance.setter
    def radial_internal_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RadialInternalClearance = value

    @property
    def radial_internal_clearance_tolerance_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RadialInternalClearanceToleranceFactor' is the original name of this property."""

        temp = self.wrapped.RadialInternalClearanceToleranceFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @radial_internal_clearance_tolerance_factor.setter
    def radial_internal_clearance_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RadialInternalClearanceToleranceFactor = value

    @property
    def refine_grid_around_contact_point(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'RefineGridAroundContactPoint' is the original name of this property."""

        temp = self.wrapped.RefineGridAroundContactPoint

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @refine_grid_around_contact_point.setter
    def refine_grid_around_contact_point(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.RefineGridAroundContactPoint = value

    @property
    def ring_ovality_scaling(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RingOvalityScaling' is the original name of this property."""

        temp = self.wrapped.RingOvalityScaling

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @ring_ovality_scaling.setter
    def ring_ovality_scaling(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RingOvalityScaling = value

    @property
    def roller_analysis_method(self) -> 'overridable.Overridable_RollerAnalysisMethod':
        """overridable.Overridable_RollerAnalysisMethod: 'RollerAnalysisMethod' is the original name of this property."""

        temp = self.wrapped.RollerAnalysisMethod

        if temp is None:
            return None

        value = overridable.Overridable_RollerAnalysisMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @roller_analysis_method.setter
    def roller_analysis_method(self, value: 'overridable.Overridable_RollerAnalysisMethod.implicit_type()'):
        wrapper_type = overridable.Overridable_RollerAnalysisMethod.wrapper_type()
        enclosed_type = overridable.Overridable_RollerAnalysisMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.RollerAnalysisMethod = value

    @property
    def rolling_frictional_moment_factor_for_newly_greased_bearing(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RollingFrictionalMomentFactorForNewlyGreasedBearing' is the original name of this property."""

        temp = self.wrapped.RollingFrictionalMomentFactorForNewlyGreasedBearing

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @rolling_frictional_moment_factor_for_newly_greased_bearing.setter
    def rolling_frictional_moment_factor_for_newly_greased_bearing(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RollingFrictionalMomentFactorForNewlyGreasedBearing = value

    @property
    def use_design_friction_coefficients(self) -> 'bool':
        """bool: 'UseDesignFrictionCoefficients' is the original name of this property."""

        temp = self.wrapped.UseDesignFrictionCoefficients

        if temp is None:
            return None

        return temp

    @use_design_friction_coefficients.setter
    def use_design_friction_coefficients(self, value: 'bool'):
        self.wrapped.UseDesignFrictionCoefficients = bool(value) if value else False

    @property
    def use_element_contact_angles_for_angular_velocities_in_ball_bearing(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'UseElementContactAnglesForAngularVelocitiesInBallBearing' is the original name of this property."""

        temp = self.wrapped.UseElementContactAnglesForAngularVelocitiesInBallBearing

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @use_element_contact_angles_for_angular_velocities_in_ball_bearing.setter
    def use_element_contact_angles_for_angular_velocities_in_ball_bearing(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.UseElementContactAnglesForAngularVelocitiesInBallBearing = value

    @property
    def use_node_per_row_inner(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'UseNodePerRowInner' is the original name of this property."""

        temp = self.wrapped.UseNodePerRowInner

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @use_node_per_row_inner.setter
    def use_node_per_row_inner(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.UseNodePerRowInner = value

    @property
    def use_node_per_row_outer(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'UseNodePerRowOuter' is the original name of this property."""

        temp = self.wrapped.UseNodePerRowOuter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @use_node_per_row_outer.setter
    def use_node_per_row_outer(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.UseNodePerRowOuter = value

    @property
    def use_specified_contact_stiffness(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'UseSpecifiedContactStiffness' is the original name of this property."""

        temp = self.wrapped.UseSpecifiedContactStiffness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @use_specified_contact_stiffness.setter
    def use_specified_contact_stiffness(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.UseSpecifiedContactStiffness = value

    @property
    def viscosity_ratio(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ViscosityRatio' is the original name of this property."""

        temp = self.wrapped.ViscosityRatio

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @viscosity_ratio.setter
    def viscosity_ratio(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ViscosityRatio = value

    @property
    def x_stiffness(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'XStiffness' is the original name of this property."""

        temp = self.wrapped.XStiffness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @x_stiffness.setter
    def x_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.XStiffness = value

    @property
    def y_stiffness(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'YStiffness' is the original name of this property."""

        temp = self.wrapped.YStiffness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @y_stiffness.setter
    def y_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.YStiffness = value

    @property
    def component_design(self) -> '_2191.Bearing':
        """Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def force_at_zero_displacement(self) -> '_1371.VectorWithLinearAndAngularComponents':
        """VectorWithLinearAndAngularComponents: 'ForceAtZeroDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceAtZeroDisplacement

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def friction_coefficients(self) -> '_1829.RollingBearingFrictionCoefficients':
        """RollingBearingFrictionCoefficients: 'FrictionCoefficients' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrictionCoefficients

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_ring_detail(self) -> '_1678.RaceDetail':
        """RaceDetail: 'InnerRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerRingDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_support_detail(self) -> '_1684.SupportDetail':
        """SupportDetail: 'InnerSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerSupportDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def left_ring_detail(self) -> '_1678.RaceDetail':
        """RaceDetail: 'LeftRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftRingDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def left_support_detail(self) -> '_1684.SupportDetail':
        """SupportDetail: 'LeftSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftSupportDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_ring_detail(self) -> '_1678.RaceDetail':
        """RaceDetail: 'OuterRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterRingDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_support_detail(self) -> '_1684.SupportDetail':
        """SupportDetail: 'OuterSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSupportDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_ring_detail(self) -> '_1678.RaceDetail':
        """RaceDetail: 'RightRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightRingDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_support_detail(self) -> '_1684.SupportDetail':
        """SupportDetail: 'RightSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightSupportDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[BearingLoadCase]':
        """List[BearingLoadCase]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def specified_stiffness_for_linear_bearing_in_local_coordinate_system(self) -> 'List[List[float]]':
        """List[List[float]]: 'SpecifiedStiffnessForLinearBearingInLocalCoordinateSystem' is the original name of this property."""

        temp = self.wrapped.SpecifiedStiffnessForLinearBearingInLocalCoordinateSystem

        if temp is None:
            return None

        value = conversion.pn_to_mp_list_float_2d(temp)
        return value

    @specified_stiffness_for_linear_bearing_in_local_coordinate_system.setter
    def specified_stiffness_for_linear_bearing_in_local_coordinate_system(self, value: 'List[List[float]]'):
        value = value if value else None
        value = conversion.mp_to_pn_list_float_2d(value)
        self.wrapped.SpecifiedStiffnessForLinearBearingInLocalCoordinateSystem = value
