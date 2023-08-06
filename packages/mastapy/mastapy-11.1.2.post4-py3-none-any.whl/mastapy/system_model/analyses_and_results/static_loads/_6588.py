"""_6588.py

CylindricalGearSetLoadCase
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears import _291
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.materials.efficiency import _268
from mastapy.system_model.analyses_and_results.static_loads import (
    _6668, _6584, _6586, _6587,
    _6619
)
from mastapy.system_model.part_model.gears import _2275, _2291
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical import _1020
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1064
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CylindricalGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetLoadCase',)


class CylindricalGearSetLoadCase(_6619.GearSetLoadCase):
    """CylindricalGearSetLoadCase

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_SET_LOAD_CASE

    def __init__(self, instance_to_wrap: 'CylindricalGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def boost_pressure(self) -> 'float':
        """float: 'BoostPressure' is the original name of this property."""

        temp = self.wrapped.BoostPressure

        if temp is None:
            return None

        return temp

    @boost_pressure.setter
    def boost_pressure(self, value: 'float'):
        self.wrapped.BoostPressure = float(value) if value else 0.0

    @property
    def coefficient_of_friction_calculation_method(self) -> '_291.CoefficientOfFrictionCalculationMethod':
        """CoefficientOfFrictionCalculationMethod: 'CoefficientOfFrictionCalculationMethod' is the original name of this property."""

        temp = self.wrapped.CoefficientOfFrictionCalculationMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_291.CoefficientOfFrictionCalculationMethod)(value) if value is not None else None

    @coefficient_of_friction_calculation_method.setter
    def coefficient_of_friction_calculation_method(self, value: '_291.CoefficientOfFrictionCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CoefficientOfFrictionCalculationMethod = value

    @property
    def dynamic_load_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DynamicLoadFactor' is the original name of this property."""

        temp = self.wrapped.DynamicLoadFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @dynamic_load_factor.setter
    def dynamic_load_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DynamicLoadFactor = value

    @property
    def efficiency_rating_method(self) -> 'overridable.Overridable_EfficiencyRatingMethod':
        """overridable.Overridable_EfficiencyRatingMethod: 'EfficiencyRatingMethod' is the original name of this property."""

        temp = self.wrapped.EfficiencyRatingMethod

        if temp is None:
            return None

        value = overridable.Overridable_EfficiencyRatingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @efficiency_rating_method.setter
    def efficiency_rating_method(self, value: 'overridable.Overridable_EfficiencyRatingMethod.implicit_type()'):
        wrapper_type = overridable.Overridable_EfficiencyRatingMethod.wrapper_type()
        enclosed_type = overridable.Overridable_EfficiencyRatingMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.EfficiencyRatingMethod = value

    @property
    def override_micro_geometry(self) -> 'bool':
        """bool: 'OverrideMicroGeometry' is the original name of this property."""

        temp = self.wrapped.OverrideMicroGeometry

        if temp is None:
            return None

        return temp

    @override_micro_geometry.setter
    def override_micro_geometry(self, value: 'bool'):
        self.wrapped.OverrideMicroGeometry = bool(value) if value else False

    @property
    def reset_micro_geometry(self) -> '_6668.ResetMicroGeometryOptions':
        """ResetMicroGeometryOptions: 'ResetMicroGeometry' is the original name of this property."""

        temp = self.wrapped.ResetMicroGeometry

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_6668.ResetMicroGeometryOptions)(value) if value is not None else None

    @reset_micro_geometry.setter
    def reset_micro_geometry(self, value: '_6668.ResetMicroGeometryOptions'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ResetMicroGeometry = value

    @property
    def use_design_coefficient_of_friction_calculation_method(self) -> 'bool':
        """bool: 'UseDesignCoefficientOfFrictionCalculationMethod' is the original name of this property."""

        temp = self.wrapped.UseDesignCoefficientOfFrictionCalculationMethod

        if temp is None:
            return None

        return temp

    @use_design_coefficient_of_friction_calculation_method.setter
    def use_design_coefficient_of_friction_calculation_method(self, value: 'bool'):
        self.wrapped.UseDesignCoefficientOfFrictionCalculationMethod = bool(value) if value else False

    @property
    def use_design_default_ltca_settings(self) -> 'bool':
        """bool: 'UseDesignDefaultLTCASettings' is the original name of this property."""

        temp = self.wrapped.UseDesignDefaultLTCASettings

        if temp is None:
            return None

        return temp

    @use_design_default_ltca_settings.setter
    def use_design_default_ltca_settings(self, value: 'bool'):
        self.wrapped.UseDesignDefaultLTCASettings = bool(value) if value else False

    @property
    def assembly_design(self) -> '_2275.CylindricalGearSet':
        """CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        if _2275.CylindricalGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def ltca(self) -> '_1020.LTCALoadCaseModifiableSettings':
        """LTCALoadCaseModifiableSettings: 'LTCA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LTCA

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def overridden_micro_geometry(self) -> '_1064.CylindricalGearSetMicroGeometry':
        """CylindricalGearSetMicroGeometry: 'OverriddenMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverriddenMicroGeometry

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gears(self) -> 'List[_6584.CylindricalGearLoadCase]':
        """List[CylindricalGearLoadCase]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_gears_load_case(self) -> 'List[_6584.CylindricalGearLoadCase]':
        """List[CylindricalGearLoadCase]: 'CylindricalGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearsLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_meshes_load_case(self) -> 'List[_6586.CylindricalGearMeshLoadCase]':
        """List[CylindricalGearMeshLoadCase]: 'CylindricalMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshesLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def get_harmonic_load_data_for_import(self) -> '_6587.CylindricalGearSetHarmonicLoadData':
        """ 'GetHarmonicLoadDataForImport' is the original name of this method.

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetHarmonicLoadData
        """

        method_result = self.wrapped.GetHarmonicLoadDataForImport()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
