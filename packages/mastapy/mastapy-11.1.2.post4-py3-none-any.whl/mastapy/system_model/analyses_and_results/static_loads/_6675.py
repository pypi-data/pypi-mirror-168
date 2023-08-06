"""_6675.py

RootAssemblyLoadCase
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.part_model import _2224
from mastapy.nodal_analysis.varying_input_components import _91, _90, _95
from mastapy.math_utility.control import _1381
from mastapy.system_model.analyses_and_results.static_loads import (
    _6528, _6535, _6588, _6542
)
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4127
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RootAssemblyLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyLoadCase',)


class RootAssemblyLoadCase(_6542.AssemblyLoadCase):
    """RootAssemblyLoadCase

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_LOAD_CASE

    def __init__(self, instance_to_wrap: 'RootAssemblyLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def brake_force_gain(self) -> 'float':
        """float: 'BrakeForceGain' is the original name of this property."""

        temp = self.wrapped.BrakeForceGain

        if temp is None:
            return None

        return temp

    @brake_force_gain.setter
    def brake_force_gain(self, value: 'float'):
        self.wrapped.BrakeForceGain = float(value) if value else 0.0

    @property
    def max_brake_force(self) -> 'float':
        """float: 'MaxBrakeForce' is the original name of this property."""

        temp = self.wrapped.MaxBrakeForce

        if temp is None:
            return None

        return temp

    @max_brake_force.setter
    def max_brake_force(self, value: 'float'):
        self.wrapped.MaxBrakeForce = float(value) if value else 0.0

    @property
    def oil_initial_temperature(self) -> 'float':
        """float: 'OilInitialTemperature' is the original name of this property."""

        temp = self.wrapped.OilInitialTemperature

        if temp is None:
            return None

        return temp

    @oil_initial_temperature.setter
    def oil_initial_temperature(self, value: 'float'):
        self.wrapped.OilInitialTemperature = float(value) if value else 0.0

    @property
    def rayleigh_damping_alpha(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RayleighDampingAlpha' is the original name of this property."""

        temp = self.wrapped.RayleighDampingAlpha

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @rayleigh_damping_alpha.setter
    def rayleigh_damping_alpha(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RayleighDampingAlpha = value

    @property
    def assembly_design(self) -> '_2224.RootAssembly':
        """RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def brake_force_input_values(self) -> '_91.ForceInputComponent':
        """ForceInputComponent: 'BrakeForceInputValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BrakeForceInputValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def drive_cycle_pid_control_settings(self) -> '_1381.PIDControlSettings':
        """PIDControlSettings: 'DriveCyclePIDControlSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DriveCyclePIDControlSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def load_case(self) -> '_6528.StaticLoadCase':
        """StaticLoadCase: 'LoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadCase

        if temp is None:
            return None

        if _6528.StaticLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast load_case to StaticLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def road_incline_input_values(self) -> '_90.AngleInputComponent':
        """AngleInputComponent: 'RoadInclineInputValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoadInclineInputValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def target_vehicle_speed(self) -> '_95.VelocityInputComponent':
        """VelocityInputComponent: 'TargetVehicleSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TargetVehicleSpeed

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def supercharger_rotor_sets(self) -> 'List[_6588.CylindricalGearSetLoadCase]':
        """List[CylindricalGearSetLoadCase]: 'SuperchargerRotorSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SuperchargerRotorSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
