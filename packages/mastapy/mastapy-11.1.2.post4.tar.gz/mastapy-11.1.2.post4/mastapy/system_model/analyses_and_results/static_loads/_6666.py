"""_6666.py

PowerLoadLoadCase
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.math_utility import _1341
from mastapy._internal.implicit import overridable, list_with_selected_item, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model import _1970, _1972, _1971
from mastapy.math_utility.measured_data import _1373
from mastapy.system_model.fe import _2124
from mastapy.system_model.analyses_and_results.static_loads import _6705, _6596, _6709
from mastapy.system_model.analyses_and_results.mbd_analyses import _5250
from mastapy.nodal_analysis.varying_input_components import _93
from mastapy.system_model.part_model import _2222
from mastapy.math_utility.control import _1381
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PowerLoadLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadLoadCase',)


class PowerLoadLoadCase(_6709.VirtualComponentLoadCase):
    """PowerLoadLoadCase

    This is a mastapy class.
    """

    TYPE = _POWER_LOAD_LOAD_CASE

    def __init__(self, instance_to_wrap: 'PowerLoadLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def constant_resistance_coefficient(self) -> 'float':
        """float: 'ConstantResistanceCoefficient' is the original name of this property."""

        temp = self.wrapped.ConstantResistanceCoefficient

        if temp is None:
            return None

        return temp

    @constant_resistance_coefficient.setter
    def constant_resistance_coefficient(self, value: 'float'):
        self.wrapped.ConstantResistanceCoefficient = float(value) if value else 0.0

    @property
    def constant_resistance_coefficient_time_profile(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'ConstantResistanceCoefficientTimeProfile' is the original name of this property."""

        temp = self.wrapped.ConstantResistanceCoefficientTimeProfile

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @constant_resistance_coefficient_time_profile.setter
    def constant_resistance_coefficient_time_profile(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.ConstantResistanceCoefficientTimeProfile = value

    @property
    def constant_torque(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ConstantTorque' is the original name of this property."""

        temp = self.wrapped.ConstantTorque

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @constant_torque.setter
    def constant_torque(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ConstantTorque = value

    @property
    def drag_torque_specification_method(self) -> '_1970.PowerLoadDragTorqueSpecificationMethod':
        """PowerLoadDragTorqueSpecificationMethod: 'DragTorqueSpecificationMethod' is the original name of this property."""

        temp = self.wrapped.DragTorqueSpecificationMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1970.PowerLoadDragTorqueSpecificationMethod)(value) if value is not None else None

    @drag_torque_specification_method.setter
    def drag_torque_specification_method(self, value: '_1970.PowerLoadDragTorqueSpecificationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DragTorqueSpecificationMethod = value

    @property
    def drag_torque_vs_speed_and_time(self) -> '_1373.GriddedSurfaceAccessor':
        """GriddedSurfaceAccessor: 'DragTorqueVsSpeedAndTime' is the original name of this property."""

        temp = self.wrapped.DragTorqueVsSpeedAndTime

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @drag_torque_vs_speed_and_time.setter
    def drag_torque_vs_speed_and_time(self, value: '_1373.GriddedSurfaceAccessor'):
        value = value.wrapped if value else None
        self.wrapped.DragTorqueVsSpeedAndTime = value

    @property
    def dynamic_torsional_stiffness(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DynamicTorsionalStiffness' is the original name of this property."""

        temp = self.wrapped.DynamicTorsionalStiffness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @dynamic_torsional_stiffness.setter
    def dynamic_torsional_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DynamicTorsionalStiffness = value

    @property
    def electric_machine_data_set_selector(self) -> 'list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet':
        """list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet: 'ElectricMachineDataSetSelector' is the original name of this property."""

        temp = self.wrapped.ElectricMachineDataSetSelector

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet)(temp) if temp is not None else None

    @electric_machine_data_set_selector.setter
    def electric_machine_data_set_selector(self, value: 'list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ElectricMachineDataSetSelector = value

    @property
    def engine_throttle_position(self) -> 'float':
        """float: 'EngineThrottlePosition' is the original name of this property."""

        temp = self.wrapped.EngineThrottlePosition

        if temp is None:
            return None

        return temp

    @engine_throttle_position.setter
    def engine_throttle_position(self, value: 'float'):
        self.wrapped.EngineThrottlePosition = float(value) if value else 0.0

    @property
    def engine_throttle_time_profile(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'EngineThrottleTimeProfile' is the original name of this property."""

        temp = self.wrapped.EngineThrottleTimeProfile

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @engine_throttle_time_profile.setter
    def engine_throttle_time_profile(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.EngineThrottleTimeProfile = value

    @property
    def first_order_lag_cutoff_frequency(self) -> 'float':
        """float: 'FirstOrderLagCutoffFrequency' is the original name of this property."""

        temp = self.wrapped.FirstOrderLagCutoffFrequency

        if temp is None:
            return None

        return temp

    @first_order_lag_cutoff_frequency.setter
    def first_order_lag_cutoff_frequency(self, value: 'float'):
        self.wrapped.FirstOrderLagCutoffFrequency = float(value) if value else 0.0

    @property
    def first_order_lag_time_constant(self) -> 'float':
        """float: 'FirstOrderLagTimeConstant' is the original name of this property."""

        temp = self.wrapped.FirstOrderLagTimeConstant

        if temp is None:
            return None

        return temp

    @first_order_lag_time_constant.setter
    def first_order_lag_time_constant(self, value: 'float'):
        self.wrapped.FirstOrderLagTimeConstant = float(value) if value else 0.0

    @property
    def initial_angular_acceleration(self) -> 'float':
        """float: 'InitialAngularAcceleration' is the original name of this property."""

        temp = self.wrapped.InitialAngularAcceleration

        if temp is None:
            return None

        return temp

    @initial_angular_acceleration.setter
    def initial_angular_acceleration(self, value: 'float'):
        self.wrapped.InitialAngularAcceleration = float(value) if value else 0.0

    @property
    def initial_angular_displacement(self) -> 'float':
        """float: 'InitialAngularDisplacement' is the original name of this property."""

        temp = self.wrapped.InitialAngularDisplacement

        if temp is None:
            return None

        return temp

    @initial_angular_displacement.setter
    def initial_angular_displacement(self, value: 'float'):
        self.wrapped.InitialAngularDisplacement = float(value) if value else 0.0

    @property
    def initial_angular_velocity(self) -> 'float':
        """float: 'InitialAngularVelocity' is the original name of this property."""

        temp = self.wrapped.InitialAngularVelocity

        if temp is None:
            return None

        return temp

    @initial_angular_velocity.setter
    def initial_angular_velocity(self, value: 'float'):
        self.wrapped.InitialAngularVelocity = float(value) if value else 0.0

    @property
    def is_wheel_using_static_friction_initially(self) -> 'bool':
        """bool: 'IsWheelUsingStaticFrictionInitially' is the original name of this property."""

        temp = self.wrapped.IsWheelUsingStaticFrictionInitially

        if temp is None:
            return None

        return temp

    @is_wheel_using_static_friction_initially.setter
    def is_wheel_using_static_friction_initially(self, value: 'bool'):
        self.wrapped.IsWheelUsingStaticFrictionInitially = bool(value) if value else False

    @property
    def linear_resistance_coefficient(self) -> 'float':
        """float: 'LinearResistanceCoefficient' is the original name of this property."""

        temp = self.wrapped.LinearResistanceCoefficient

        if temp is None:
            return None

        return temp

    @linear_resistance_coefficient.setter
    def linear_resistance_coefficient(self, value: 'float'):
        self.wrapped.LinearResistanceCoefficient = float(value) if value else 0.0

    @property
    def linear_resistance_coefficient_time_profile(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'LinearResistanceCoefficientTimeProfile' is the original name of this property."""

        temp = self.wrapped.LinearResistanceCoefficientTimeProfile

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @linear_resistance_coefficient_time_profile.setter
    def linear_resistance_coefficient_time_profile(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.LinearResistanceCoefficientTimeProfile = value

    @property
    def maximum_throttle_in_drive_cycle(self) -> 'float':
        """float: 'MaximumThrottleInDriveCycle' is the original name of this property."""

        temp = self.wrapped.MaximumThrottleInDriveCycle

        if temp is None:
            return None

        return temp

    @maximum_throttle_in_drive_cycle.setter
    def maximum_throttle_in_drive_cycle(self, value: 'float'):
        self.wrapped.MaximumThrottleInDriveCycle = float(value) if value else 0.0

    @property
    def power(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Power' is the original name of this property."""

        temp = self.wrapped.Power

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @power.setter
    def power(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Power = value

    @property
    def power_load_for_pid_control(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'PowerLoadForPIDControl' is the original name of this property."""

        temp = self.wrapped.PowerLoadForPIDControl

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @power_load_for_pid_control.setter
    def power_load_for_pid_control(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.PowerLoadForPIDControl = value

    @property
    def proportion_of_vehicle_weight_carried(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ProportionOfVehicleWeightCarried' is the original name of this property."""

        temp = self.wrapped.ProportionOfVehicleWeightCarried

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @proportion_of_vehicle_weight_carried.setter
    def proportion_of_vehicle_weight_carried(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ProportionOfVehicleWeightCarried = value

    @property
    def quadratic_resistance_coefficient(self) -> 'float':
        """float: 'QuadraticResistanceCoefficient' is the original name of this property."""

        temp = self.wrapped.QuadraticResistanceCoefficient

        if temp is None:
            return None

        return temp

    @quadratic_resistance_coefficient.setter
    def quadratic_resistance_coefficient(self, value: 'float'):
        self.wrapped.QuadraticResistanceCoefficient = float(value) if value else 0.0

    @property
    def quadratic_resistance_coefficient_time_profile(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'QuadraticResistanceCoefficientTimeProfile' is the original name of this property."""

        temp = self.wrapped.QuadraticResistanceCoefficientTimeProfile

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @quadratic_resistance_coefficient_time_profile.setter
    def quadratic_resistance_coefficient_time_profile(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.QuadraticResistanceCoefficientTimeProfile = value

    @property
    def specified_angle_for_input_torque(self) -> 'float':
        """float: 'SpecifiedAngleForInputTorque' is the original name of this property."""

        temp = self.wrapped.SpecifiedAngleForInputTorque

        if temp is None:
            return None

        return temp

    @specified_angle_for_input_torque.setter
    def specified_angle_for_input_torque(self, value: 'float'):
        self.wrapped.SpecifiedAngleForInputTorque = float(value) if value else 0.0

    @property
    def specified_time_for_input_torque(self) -> 'float':
        """float: 'SpecifiedTimeForInputTorque' is the original name of this property."""

        temp = self.wrapped.SpecifiedTimeForInputTorque

        if temp is None:
            return None

        return temp

    @specified_time_for_input_torque.setter
    def specified_time_for_input_torque(self, value: 'float'):
        self.wrapped.SpecifiedTimeForInputTorque = float(value) if value else 0.0

    @property
    def specify_initial_acceleration(self) -> 'bool':
        """bool: 'SpecifyInitialAcceleration' is the original name of this property."""

        temp = self.wrapped.SpecifyInitialAcceleration

        if temp is None:
            return None

        return temp

    @specify_initial_acceleration.setter
    def specify_initial_acceleration(self, value: 'bool'):
        self.wrapped.SpecifyInitialAcceleration = bool(value) if value else False

    @property
    def specify_initial_displacement(self) -> 'bool':
        """bool: 'SpecifyInitialDisplacement' is the original name of this property."""

        temp = self.wrapped.SpecifyInitialDisplacement

        if temp is None:
            return None

        return temp

    @specify_initial_displacement.setter
    def specify_initial_displacement(self, value: 'bool'):
        self.wrapped.SpecifyInitialDisplacement = bool(value) if value else False

    @property
    def specify_initial_velocity(self) -> 'bool':
        """bool: 'SpecifyInitialVelocity' is the original name of this property."""

        temp = self.wrapped.SpecifyInitialVelocity

        if temp is None:
            return None

        return temp

    @specify_initial_velocity.setter
    def specify_initial_velocity(self, value: 'bool'):
        self.wrapped.SpecifyInitialVelocity = bool(value) if value else False

    @property
    def speed(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Speed' is the original name of this property."""

        temp = self.wrapped.Speed

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @speed.setter
    def speed(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Speed = value

    @property
    def speed_vs_time(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'SpeedVsTime' is the original name of this property."""

        temp = self.wrapped.SpeedVsTime

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @speed_vs_time.setter
    def speed_vs_time(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.SpeedVsTime = value

    @property
    def system_deflection_torque_also_applies_to_advanced_system_deflection(self) -> 'bool':
        """bool: 'SystemDeflectionTorqueAlsoAppliesToAdvancedSystemDeflection' is the original name of this property."""

        temp = self.wrapped.SystemDeflectionTorqueAlsoAppliesToAdvancedSystemDeflection

        if temp is None:
            return None

        return temp

    @system_deflection_torque_also_applies_to_advanced_system_deflection.setter
    def system_deflection_torque_also_applies_to_advanced_system_deflection(self, value: 'bool'):
        self.wrapped.SystemDeflectionTorqueAlsoAppliesToAdvancedSystemDeflection = bool(value) if value else False

    @property
    def system_deflection_torque_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection':
        """enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection: 'SystemDeflectionTorqueMethod' is the original name of this property."""

        temp = self.wrapped.SystemDeflectionTorqueMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @system_deflection_torque_method.setter
    def system_deflection_torque_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.SystemDeflectionTorqueMethod = value

    @property
    def target_engine_idle_speed(self) -> 'float':
        """float: 'TargetEngineIdleSpeed' is the original name of this property."""

        temp = self.wrapped.TargetEngineIdleSpeed

        if temp is None:
            return None

        return temp

    @target_engine_idle_speed.setter
    def target_engine_idle_speed(self, value: 'float'):
        self.wrapped.TargetEngineIdleSpeed = float(value) if value else 0.0

    @property
    def target_speed(self) -> 'float':
        """float: 'TargetSpeed' is the original name of this property."""

        temp = self.wrapped.TargetSpeed

        if temp is None:
            return None

        return temp

    @target_speed.setter
    def target_speed(self, value: 'float'):
        self.wrapped.TargetSpeed = float(value) if value else 0.0

    @property
    def target_speed_input_type(self) -> '_1972.PowerLoadPIDControlSpeedInputType':
        """PowerLoadPIDControlSpeedInputType: 'TargetSpeedInputType' is the original name of this property."""

        temp = self.wrapped.TargetSpeedInputType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1972.PowerLoadPIDControlSpeedInputType)(value) if value is not None else None

    @target_speed_input_type.setter
    def target_speed_input_type(self, value: '_1972.PowerLoadPIDControlSpeedInputType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TargetSpeedInputType = value

    @property
    def target_speed_vs_time(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'TargetSpeedVsTime' is the original name of this property."""

        temp = self.wrapped.TargetSpeedVsTime

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @target_speed_vs_time.setter
    def target_speed_vs_time(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.TargetSpeedVsTime = value

    @property
    def torque(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Torque' is the original name of this property."""

        temp = self.wrapped.Torque

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @torque.setter
    def torque(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Torque = value

    @property
    def torque_input_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod':
        """enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod: 'TorqueInputMethod' is the original name of this property."""

        temp = self.wrapped.TorqueInputMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @torque_input_method.setter
    def torque_input_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.TorqueInputMethod = value

    @property
    def torque_time_profile_repeats(self) -> 'bool':
        """bool: 'TorqueTimeProfileRepeats' is the original name of this property."""

        temp = self.wrapped.TorqueTimeProfileRepeats

        if temp is None:
            return None

        return temp

    @torque_time_profile_repeats.setter
    def torque_time_profile_repeats(self, value: 'bool'):
        self.wrapped.TorqueTimeProfileRepeats = bool(value) if value else False

    @property
    def torque_vs_angle(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'TorqueVsAngle' is the original name of this property."""

        temp = self.wrapped.TorqueVsAngle

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @torque_vs_angle.setter
    def torque_vs_angle(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.TorqueVsAngle = value

    @property
    def torque_vs_angle_and_speed(self) -> '_1373.GriddedSurfaceAccessor':
        """GriddedSurfaceAccessor: 'TorqueVsAngleAndSpeed' is the original name of this property."""

        temp = self.wrapped.TorqueVsAngleAndSpeed

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @torque_vs_angle_and_speed.setter
    def torque_vs_angle_and_speed(self, value: '_1373.GriddedSurfaceAccessor'):
        value = value.wrapped if value else None
        self.wrapped.TorqueVsAngleAndSpeed = value

    @property
    def torque_vs_time(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'TorqueVsTime' is the original name of this property."""

        temp = self.wrapped.TorqueVsTime

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @torque_vs_time.setter
    def torque_vs_time(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.TorqueVsTime = value

    @property
    def total_mean_rotor_x_force_over_all_nodes(self) -> 'float':
        """float: 'TotalMeanRotorXForceOverAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalMeanRotorXForceOverAllNodes

        if temp is None:
            return None

        return temp

    @property
    def total_mean_rotor_y_force_over_all_nodes(self) -> 'float':
        """float: 'TotalMeanRotorYForceOverAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalMeanRotorYForceOverAllNodes

        if temp is None:
            return None

        return temp

    @property
    def unbalanced_magnetic_pull_stiffness(self) -> 'float':
        """float: 'UnbalancedMagneticPullStiffness' is the original name of this property."""

        temp = self.wrapped.UnbalancedMagneticPullStiffness

        if temp is None:
            return None

        return temp

    @unbalanced_magnetic_pull_stiffness.setter
    def unbalanced_magnetic_pull_stiffness(self, value: 'float'):
        self.wrapped.UnbalancedMagneticPullStiffness = float(value) if value else 0.0

    @property
    def use_engine_idle_speed_control(self) -> 'bool':
        """bool: 'UseEngineIdleSpeedControl' is the original name of this property."""

        temp = self.wrapped.UseEngineIdleSpeedControl

        if temp is None:
            return None

        return temp

    @use_engine_idle_speed_control.setter
    def use_engine_idle_speed_control(self, value: 'bool'):
        self.wrapped.UseEngineIdleSpeedControl = bool(value) if value else False

    @property
    def use_time_dependent_constant_resistance_coefficient(self) -> 'bool':
        """bool: 'UseTimeDependentConstantResistanceCoefficient' is the original name of this property."""

        temp = self.wrapped.UseTimeDependentConstantResistanceCoefficient

        if temp is None:
            return None

        return temp

    @use_time_dependent_constant_resistance_coefficient.setter
    def use_time_dependent_constant_resistance_coefficient(self, value: 'bool'):
        self.wrapped.UseTimeDependentConstantResistanceCoefficient = bool(value) if value else False

    @property
    def use_time_dependent_linear_resistance_coefficient(self) -> 'bool':
        """bool: 'UseTimeDependentLinearResistanceCoefficient' is the original name of this property."""

        temp = self.wrapped.UseTimeDependentLinearResistanceCoefficient

        if temp is None:
            return None

        return temp

    @use_time_dependent_linear_resistance_coefficient.setter
    def use_time_dependent_linear_resistance_coefficient(self, value: 'bool'):
        self.wrapped.UseTimeDependentLinearResistanceCoefficient = bool(value) if value else False

    @property
    def use_time_dependent_quadratic_resistance_coefficient(self) -> 'bool':
        """bool: 'UseTimeDependentQuadraticResistanceCoefficient' is the original name of this property."""

        temp = self.wrapped.UseTimeDependentQuadraticResistanceCoefficient

        if temp is None:
            return None

        return temp

    @use_time_dependent_quadratic_resistance_coefficient.setter
    def use_time_dependent_quadratic_resistance_coefficient(self, value: 'bool'):
        self.wrapped.UseTimeDependentQuadraticResistanceCoefficient = bool(value) if value else False

    @property
    def use_time_dependent_throttle(self) -> 'bool':
        """bool: 'UseTimeDependentThrottle' is the original name of this property."""

        temp = self.wrapped.UseTimeDependentThrottle

        if temp is None:
            return None

        return temp

    @use_time_dependent_throttle.setter
    def use_time_dependent_throttle(self, value: 'bool'):
        self.wrapped.UseTimeDependentThrottle = bool(value) if value else False

    @property
    def vehicle_speed_to_start_idle_control(self) -> 'float':
        """float: 'VehicleSpeedToStartIdleControl' is the original name of this property."""

        temp = self.wrapped.VehicleSpeedToStartIdleControl

        if temp is None:
            return None

        return temp

    @vehicle_speed_to_start_idle_control.setter
    def vehicle_speed_to_start_idle_control(self, value: 'float'):
        self.wrapped.VehicleSpeedToStartIdleControl = float(value) if value else 0.0

    @property
    def vehicle_speed_to_stop_idle_control(self) -> 'float':
        """float: 'VehicleSpeedToStopIdleControl' is the original name of this property."""

        temp = self.wrapped.VehicleSpeedToStopIdleControl

        if temp is None:
            return None

        return temp

    @vehicle_speed_to_stop_idle_control.setter
    def vehicle_speed_to_stop_idle_control(self, value: 'float'):
        self.wrapped.VehicleSpeedToStopIdleControl = float(value) if value else 0.0

    @property
    def wheel_slip_model(self) -> '_5250.WheelSlipType':
        """WheelSlipType: 'WheelSlipModel' is the original name of this property."""

        temp = self.wrapped.WheelSlipModel

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5250.WheelSlipType)(value) if value is not None else None

    @wheel_slip_model.setter
    def wheel_slip_model(self, value: '_5250.WheelSlipType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.WheelSlipModel = value

    @property
    def wheel_static_to_dynamic_friction_ratio(self) -> 'float':
        """float: 'WheelStaticToDynamicFrictionRatio' is the original name of this property."""

        temp = self.wrapped.WheelStaticToDynamicFrictionRatio

        if temp is None:
            return None

        return temp

    @wheel_static_to_dynamic_friction_ratio.setter
    def wheel_static_to_dynamic_friction_ratio(self, value: 'float'):
        self.wrapped.WheelStaticToDynamicFrictionRatio = float(value) if value else 0.0

    @property
    def wheel_to_vehicle_stiffness(self) -> 'float':
        """float: 'WheelToVehicleStiffness' is the original name of this property."""

        temp = self.wrapped.WheelToVehicleStiffness

        if temp is None:
            return None

        return temp

    @wheel_to_vehicle_stiffness.setter
    def wheel_to_vehicle_stiffness(self, value: 'float'):
        self.wrapped.WheelToVehicleStiffness = float(value) if value else 0.0

    @property
    def coefficient_of_friction_with_ground(self) -> '_93.NonDimensionalInputComponent':
        """NonDimensionalInputComponent: 'CoefficientOfFrictionWithGround' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoefficientOfFrictionWithGround

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_design(self) -> '_2222.PowerLoad':
        """PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def engine_idle_speed_control_pid_settings(self) -> '_1381.PIDControlSettings':
        """PIDControlSettings: 'EngineIdleSpeedControlPIDSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EngineIdleSpeedControlPIDSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def pid_control_settings(self) -> '_1381.PIDControlSettings':
        """PIDControlSettings: 'PIDControlSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PIDControlSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def get_harmonic_load_data_for_import(self) -> '_6596.ElectricMachineHarmonicLoadData':
        """ 'GetHarmonicLoadDataForImport' is the original name of this method.

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ElectricMachineHarmonicLoadData
        """

        method_result = self.wrapped.GetHarmonicLoadDataForImport()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
