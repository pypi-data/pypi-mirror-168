"""_6701.py

TorqueConverterLoadCase
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.math_utility import _1341
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.system_model.analyses_and_results.mbd_analyses import _5243
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.part_model.couplings import _2356
from mastapy.system_model.analyses_and_results.static_loads import _6576
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'TorqueConverterLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterLoadCase',)


class TorqueConverterLoadCase(_6576.CouplingLoadCase):
    """TorqueConverterLoadCase

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_LOAD_CASE

    def __init__(self, instance_to_wrap: 'TorqueConverterLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def initial_lock_up_clutch_temperature(self) -> 'float':
        """float: 'InitialLockUpClutchTemperature' is the original name of this property."""

        temp = self.wrapped.InitialLockUpClutchTemperature

        if temp is None:
            return None

        return temp

    @initial_lock_up_clutch_temperature.setter
    def initial_lock_up_clutch_temperature(self, value: 'float'):
        self.wrapped.InitialLockUpClutchTemperature = float(value) if value else 0.0

    @property
    def initially_locked(self) -> 'bool':
        """bool: 'InitiallyLocked' is the original name of this property."""

        temp = self.wrapped.InitiallyLocked

        if temp is None:
            return None

        return temp

    @initially_locked.setter
    def initially_locked(self, value: 'bool'):
        self.wrapped.InitiallyLocked = bool(value) if value else False

    @property
    def lock_up_clutch_pressure_for_no_torque_converter_operation(self) -> 'float':
        """float: 'LockUpClutchPressureForNoTorqueConverterOperation' is the original name of this property."""

        temp = self.wrapped.LockUpClutchPressureForNoTorqueConverterOperation

        if temp is None:
            return None

        return temp

    @lock_up_clutch_pressure_for_no_torque_converter_operation.setter
    def lock_up_clutch_pressure_for_no_torque_converter_operation(self, value: 'float'):
        self.wrapped.LockUpClutchPressureForNoTorqueConverterOperation = float(value) if value else 0.0

    @property
    def lock_up_clutch_pressure_time_profile(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'LockUpClutchPressureTimeProfile' is the original name of this property."""

        temp = self.wrapped.LockUpClutchPressureTimeProfile

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @lock_up_clutch_pressure_time_profile.setter
    def lock_up_clutch_pressure_time_profile(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.LockUpClutchPressureTimeProfile = value

    @property
    def lock_up_clutch_rule(self) -> 'enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule':
        """enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule: 'LockUpClutchRule' is the original name of this property."""

        temp = self.wrapped.LockUpClutchRule

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @lock_up_clutch_rule.setter
    def lock_up_clutch_rule(self, value: 'enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LockUpClutchRule = value

    @property
    def locking_speed_ratio_threshold(self) -> 'float':
        """float: 'LockingSpeedRatioThreshold' is the original name of this property."""

        temp = self.wrapped.LockingSpeedRatioThreshold

        if temp is None:
            return None

        return temp

    @locking_speed_ratio_threshold.setter
    def locking_speed_ratio_threshold(self, value: 'float'):
        self.wrapped.LockingSpeedRatioThreshold = float(value) if value else 0.0

    @property
    def time_for_full_clutch_pressure(self) -> 'float':
        """float: 'TimeForFullClutchPressure' is the original name of this property."""

        temp = self.wrapped.TimeForFullClutchPressure

        if temp is None:
            return None

        return temp

    @time_for_full_clutch_pressure.setter
    def time_for_full_clutch_pressure(self, value: 'float'):
        self.wrapped.TimeForFullClutchPressure = float(value) if value else 0.0

    @property
    def time_to_change_locking_state(self) -> 'float':
        """float: 'TimeToChangeLockingState' is the original name of this property."""

        temp = self.wrapped.TimeToChangeLockingState

        if temp is None:
            return None

        return temp

    @time_to_change_locking_state.setter
    def time_to_change_locking_state(self, value: 'float'):
        self.wrapped.TimeToChangeLockingState = float(value) if value else 0.0

    @property
    def transient_time_to_change_locking_status(self) -> 'float':
        """float: 'TransientTimeToChangeLockingStatus' is the original name of this property."""

        temp = self.wrapped.TransientTimeToChangeLockingStatus

        if temp is None:
            return None

        return temp

    @transient_time_to_change_locking_status.setter
    def transient_time_to_change_locking_status(self, value: 'float'):
        self.wrapped.TransientTimeToChangeLockingStatus = float(value) if value else 0.0

    @property
    def vehicle_speed_to_unlock(self) -> 'float':
        """float: 'VehicleSpeedToUnlock' is the original name of this property."""

        temp = self.wrapped.VehicleSpeedToUnlock

        if temp is None:
            return None

        return temp

    @vehicle_speed_to_unlock.setter
    def vehicle_speed_to_unlock(self, value: 'float'):
        self.wrapped.VehicleSpeedToUnlock = float(value) if value else 0.0

    @property
    def assembly_design(self) -> '_2356.TorqueConverter':
        """TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
