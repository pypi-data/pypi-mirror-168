"""_982.py

CylindricalGearMeshDesign
"""


from typing import List

from PIL.Image import Image

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears import _290, _307
from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.gear_designs.cylindrical import (
    _989, _1048, _962, _990,
    _1001, _983, _975, _998,
    _1002
)
from mastapy._internal.cast_exception import CastException
from mastapy.math_utility.measured_ranges import _1372
from mastapy.gears.gear_designs import _912
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshDesign',)


class CylindricalGearMeshDesign(_912.GearMeshDesign):
    """CylindricalGearMeshDesign

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_DESIGN

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_contact_ratio(self) -> 'float':
        """float: 'AxialContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialContactRatio

        if temp is None:
            return None

        return temp

    @property
    def bearing_span(self) -> 'float':
        """float: 'BearingSpan' is the original name of this property."""

        temp = self.wrapped.BearingSpan

        if temp is None:
            return None

        return temp

    @bearing_span.setter
    def bearing_span(self, value: 'float'):
        self.wrapped.BearingSpan = float(value) if value else 0.0

    @property
    def centre_distance(self) -> 'float':
        """float: 'CentreDistance' is the original name of this property."""

        temp = self.wrapped.CentreDistance

        if temp is None:
            return None

        return temp

    @centre_distance.setter
    def centre_distance(self, value: 'float'):
        self.wrapped.CentreDistance = float(value) if value else 0.0

    @property
    def centre_distance_calculating_gear_teeth_numbers(self) -> 'float':
        """float: 'CentreDistanceCalculatingGearTeethNumbers' is the original name of this property."""

        temp = self.wrapped.CentreDistanceCalculatingGearTeethNumbers

        if temp is None:
            return None

        return temp

    @centre_distance_calculating_gear_teeth_numbers.setter
    def centre_distance_calculating_gear_teeth_numbers(self, value: 'float'):
        self.wrapped.CentreDistanceCalculatingGearTeethNumbers = float(value) if value else 0.0

    @property
    def centre_distance_change_method(self) -> '_290.CentreDistanceChangeMethod':
        """CentreDistanceChangeMethod: 'CentreDistanceChangeMethod' is the original name of this property."""

        temp = self.wrapped.CentreDistanceChangeMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_290.CentreDistanceChangeMethod)(value) if value is not None else None

    @centre_distance_change_method.setter
    def centre_distance_change_method(self, value: '_290.CentreDistanceChangeMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CentreDistanceChangeMethod = value

    @property
    def centre_distance_at_tight_mesh_maximum_metal(self) -> 'float':
        """float: 'CentreDistanceAtTightMeshMaximumMetal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CentreDistanceAtTightMeshMaximumMetal

        if temp is None:
            return None

        return temp

    @property
    def centre_distance_at_tight_mesh_minimum_metal(self) -> 'float':
        """float: 'CentreDistanceAtTightMeshMinimumMetal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CentreDistanceAtTightMeshMinimumMetal

        if temp is None:
            return None

        return temp

    @property
    def centre_distance_with_normal_module_adjustment(self) -> 'float':
        """float: 'CentreDistanceWithNormalModuleAdjustment' is the original name of this property."""

        temp = self.wrapped.CentreDistanceWithNormalModuleAdjustment

        if temp is None:
            return None

        return temp

    @centre_distance_with_normal_module_adjustment.setter
    def centre_distance_with_normal_module_adjustment(self, value: 'float'):
        self.wrapped.CentreDistanceWithNormalModuleAdjustment = float(value) if value else 0.0

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
    def effective_face_width(self) -> 'float':
        """float: 'EffectiveFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveFaceWidth

        if temp is None:
            return None

        return temp

    @property
    def face_width_factor_for_extended_tip_contact(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FaceWidthFactorForExtendedTipContact' is the original name of this property."""

        temp = self.wrapped.FaceWidthFactorForExtendedTipContact

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @face_width_factor_for_extended_tip_contact.setter
    def face_width_factor_for_extended_tip_contact(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FaceWidthFactorForExtendedTipContact = value

    @property
    def filter_cutoff_wave_length(self) -> 'float':
        """float: 'FilterCutoffWaveLength' is the original name of this property."""

        temp = self.wrapped.FilterCutoffWaveLength

        if temp is None:
            return None

        return temp

    @filter_cutoff_wave_length.setter
    def filter_cutoff_wave_length(self, value: 'float'):
        self.wrapped.FilterCutoffWaveLength = float(value) if value else 0.0

    @property
    def gear_mesh_drawing(self) -> 'Image':
        """Image: 'GearMeshDrawing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMeshDrawing

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def heat_dissipating_surface_of_housing(self) -> 'float':
        """float: 'HeatDissipatingSurfaceOfHousing' is the original name of this property."""

        temp = self.wrapped.HeatDissipatingSurfaceOfHousing

        if temp is None:
            return None

        return temp

    @heat_dissipating_surface_of_housing.setter
    def heat_dissipating_surface_of_housing(self, value: 'float'):
        self.wrapped.HeatDissipatingSurfaceOfHousing = float(value) if value else 0.0

    @property
    def heat_transfer_resistance_of_housing(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'HeatTransferResistanceOfHousing' is the original name of this property."""

        temp = self.wrapped.HeatTransferResistanceOfHousing

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @heat_transfer_resistance_of_housing.setter
    def heat_transfer_resistance_of_housing(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.HeatTransferResistanceOfHousing = value

    @property
    def is_asymmetric(self) -> 'bool':
        """bool: 'IsAsymmetric' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsAsymmetric

        if temp is None:
            return None

        return temp

    @property
    def lubrication_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LubricationMethods':
        """enum_with_selected_value.EnumWithSelectedValue_LubricationMethods: 'LubricationMethod' is the original name of this property."""

        temp = self.wrapped.LubricationMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LubricationMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @lubrication_method.setter
    def lubrication_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LubricationMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LubricationMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LubricationMethod = value

    @property
    def percentage_of_openings_in_the_housing_surface(self) -> 'float':
        """float: 'PercentageOfOpeningsInTheHousingSurface' is the original name of this property."""

        temp = self.wrapped.PercentageOfOpeningsInTheHousingSurface

        if temp is None:
            return None

        return temp

    @percentage_of_openings_in_the_housing_surface.setter
    def percentage_of_openings_in_the_housing_surface(self, value: 'float'):
        self.wrapped.PercentageOfOpeningsInTheHousingSurface = float(value) if value else 0.0

    @property
    def pinion_offset_from_bearing(self) -> 'float':
        """float: 'PinionOffsetFromBearing' is the original name of this property."""

        temp = self.wrapped.PinionOffsetFromBearing

        if temp is None:
            return None

        return temp

    @pinion_offset_from_bearing.setter
    def pinion_offset_from_bearing(self, value: 'float'):
        self.wrapped.PinionOffsetFromBearing = float(value) if value else 0.0

    @property
    def profile_modification(self) -> '_989.CylindricalGearProfileModifications':
        """CylindricalGearProfileModifications: 'ProfileModification' is the original name of this property."""

        temp = self.wrapped.ProfileModification

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_989.CylindricalGearProfileModifications)(value) if value is not None else None

    @profile_modification.setter
    def profile_modification(self, value: '_989.CylindricalGearProfileModifications'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProfileModification = value

    @property
    def ratio(self) -> 'float':
        """float: 'Ratio' is the original name of this property."""

        temp = self.wrapped.Ratio

        if temp is None:
            return None

        return temp

    @ratio.setter
    def ratio(self, value: 'float'):
        self.wrapped.Ratio = float(value) if value else 0.0

    @property
    def reference_centre_distance(self) -> 'float':
        """float: 'ReferenceCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceCentreDistance

        if temp is None:
            return None

        return temp

    @property
    def relative_tooth_engagement_time(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RelativeToothEngagementTime' is the original name of this property."""

        temp = self.wrapped.RelativeToothEngagementTime

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @relative_tooth_engagement_time.setter
    def relative_tooth_engagement_time(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RelativeToothEngagementTime = value

    @property
    def sum_of_profile_shift_coefficient(self) -> 'float':
        """float: 'SumOfProfileShiftCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumOfProfileShiftCoefficient

        if temp is None:
            return None

        return temp

    @property
    def surface_condition_factor(self) -> 'float':
        """float: 'SurfaceConditionFactor' is the original name of this property."""

        temp = self.wrapped.SurfaceConditionFactor

        if temp is None:
            return None

        return temp

    @surface_condition_factor.setter
    def surface_condition_factor(self, value: 'float'):
        self.wrapped.SurfaceConditionFactor = float(value) if value else 0.0

    @property
    def type_of_mechanism_housing(self) -> '_1048.TypeOfMechanismHousing':
        """TypeOfMechanismHousing: 'TypeOfMechanismHousing' is the original name of this property."""

        temp = self.wrapped.TypeOfMechanismHousing

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1048.TypeOfMechanismHousing)(value) if value is not None else None

    @type_of_mechanism_housing.setter
    def type_of_mechanism_housing(self, value: '_1048.TypeOfMechanismHousing'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TypeOfMechanismHousing = value

    @property
    def user_specified_coefficient_of_friction(self) -> 'float':
        """float: 'UserSpecifiedCoefficientOfFriction' is the original name of this property."""

        temp = self.wrapped.UserSpecifiedCoefficientOfFriction

        if temp is None:
            return None

        return temp

    @user_specified_coefficient_of_friction.setter
    def user_specified_coefficient_of_friction(self, value: 'float'):
        self.wrapped.UserSpecifiedCoefficientOfFriction = float(value) if value else 0.0

    @property
    def wear_coefficient_for_a_driven_pinion(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'WearCoefficientForADrivenPinion' is the original name of this property."""

        temp = self.wrapped.WearCoefficientForADrivenPinion

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @wear_coefficient_for_a_driven_pinion.setter
    def wear_coefficient_for_a_driven_pinion(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.WearCoefficientForADrivenPinion = value

    @property
    def wear_coefficient_for_a_driving_pinion(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'WearCoefficientForADrivingPinion' is the original name of this property."""

        temp = self.wrapped.WearCoefficientForADrivingPinion

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @wear_coefficient_for_a_driving_pinion.setter
    def wear_coefficient_for_a_driving_pinion(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.WearCoefficientForADrivingPinion = value

    @property
    def working_depth(self) -> 'float':
        """float: 'WorkingDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingDepth

        if temp is None:
            return None

        return temp

    @property
    def working_helix_angle(self) -> 'float':
        """float: 'WorkingHelixAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingHelixAngle

        if temp is None:
            return None

        return temp

    @property
    def backlash_specification(self) -> '_962.BacklashSpecification':
        """BacklashSpecification: 'BacklashSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BacklashSpecification

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_set(self) -> '_990.CylindricalGearSetDesign':
        """CylindricalGearSetDesign: 'CylindricalGearSet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSet

        if temp is None:
            return None

        if _990.CylindricalGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_set to CylindricalGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def left_flank(self) -> '_983.CylindricalGearMeshFlankDesign':
        """CylindricalGearMeshFlankDesign: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_flank(self) -> '_983.CylindricalGearMeshFlankDesign':
        """CylindricalGearMeshFlankDesign: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def valid_normal_module_range(self) -> '_1372.ShortLengthRange':
        """ShortLengthRange: 'ValidNormalModuleRange' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ValidNormalModuleRange

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gears(self) -> 'List[_975.CylindricalGearDesign]':
        """List[CylindricalGearDesign]: 'CylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_meshed_gear(self) -> 'List[_998.CylindricalMeshedGear]':
        """List[CylindricalMeshedGear]: 'CylindricalMeshedGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshedGear

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def flanks(self) -> 'List[_983.CylindricalGearMeshFlankDesign]':
        """List[CylindricalGearMeshFlankDesign]: 'Flanks' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Flanks

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def both_flanks(self) -> '_983.CylindricalGearMeshFlankDesign':
        """CylindricalGearMeshFlankDesign: 'BothFlanks' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BothFlanks

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a(self) -> '_975.CylindricalGearDesign':
        """CylindricalGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _975.CylindricalGearDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b(self) -> '_975.CylindricalGearDesign':
        """CylindricalGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _975.CylindricalGearDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def center_distance_for(self, helix_angle: 'float', pressure_angle: 'float', sum_of_adden_mod: 'float', sum_of_number_of_teeth: 'float', normal_module: 'float') -> 'float':
        """ 'CenterDistanceFor' is the original name of this method.

        Args:
            helix_angle (float)
            pressure_angle (float)
            sum_of_adden_mod (float)
            sum_of_number_of_teeth (float)
            normal_module (float)

        Returns:
            float
        """

        helix_angle = float(helix_angle)
        pressure_angle = float(pressure_angle)
        sum_of_adden_mod = float(sum_of_adden_mod)
        sum_of_number_of_teeth = float(sum_of_number_of_teeth)
        normal_module = float(normal_module)
        method_result = self.wrapped.CenterDistanceFor(helix_angle if helix_angle else 0.0, pressure_angle if pressure_angle else 0.0, sum_of_adden_mod if sum_of_adden_mod else 0.0, sum_of_number_of_teeth if sum_of_number_of_teeth else 0.0, normal_module if normal_module else 0.0)
        return method_result
