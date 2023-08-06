"""_1381.py

PIDControlSettings
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.math_utility.measured_data import _1373
from mastapy.math_utility import _1329
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PID_CONTROL_SETTINGS = python_net_import('SMT.MastaAPI.MathUtility.Control', 'PIDControlSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('PIDControlSettings',)


class PIDControlSettings(_0.APIBase):
    """PIDControlSettings

    This is a mastapy class.
    """

    TYPE = _PID_CONTROL_SETTINGS

    def __init__(self, instance_to_wrap: 'PIDControlSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def control_start_time(self) -> 'float':
        """float: 'ControlStartTime' is the original name of this property."""

        temp = self.wrapped.ControlStartTime

        if temp is None:
            return None

        return temp

    @control_start_time.setter
    def control_start_time(self, value: 'float'):
        self.wrapped.ControlStartTime = float(value) if value else 0.0

    @property
    def differential_gain(self) -> 'float':
        """float: 'DifferentialGain' is the original name of this property."""

        temp = self.wrapped.DifferentialGain

        if temp is None:
            return None

        return temp

    @differential_gain.setter
    def differential_gain(self, value: 'float'):
        self.wrapped.DifferentialGain = float(value) if value else 0.0

    @property
    def differential_gain_vs_time_and_error(self) -> '_1373.GriddedSurfaceAccessor':
        """GriddedSurfaceAccessor: 'DifferentialGainVsTimeAndError' is the original name of this property."""

        temp = self.wrapped.DifferentialGainVsTimeAndError

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @differential_gain_vs_time_and_error.setter
    def differential_gain_vs_time_and_error(self, value: '_1373.GriddedSurfaceAccessor'):
        value = value.wrapped if value else None
        self.wrapped.DifferentialGainVsTimeAndError = value

    @property
    def differential_time_constant(self) -> 'float':
        """float: 'DifferentialTimeConstant' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DifferentialTimeConstant

        if temp is None:
            return None

        return temp

    @property
    def integral_gain(self) -> 'float':
        """float: 'IntegralGain' is the original name of this property."""

        temp = self.wrapped.IntegralGain

        if temp is None:
            return None

        return temp

    @integral_gain.setter
    def integral_gain(self, value: 'float'):
        self.wrapped.IntegralGain = float(value) if value else 0.0

    @property
    def integral_gain_vs_time_and_error(self) -> '_1373.GriddedSurfaceAccessor':
        """GriddedSurfaceAccessor: 'IntegralGainVsTimeAndError' is the original name of this property."""

        temp = self.wrapped.IntegralGainVsTimeAndError

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @integral_gain_vs_time_and_error.setter
    def integral_gain_vs_time_and_error(self, value: '_1373.GriddedSurfaceAccessor'):
        value = value.wrapped if value else None
        self.wrapped.IntegralGainVsTimeAndError = value

    @property
    def integral_time_constant(self) -> 'float':
        """float: 'IntegralTimeConstant' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IntegralTimeConstant

        if temp is None:
            return None

        return temp

    @property
    def max_change_in_manipulated_value_per_unit_time(self) -> 'float':
        """float: 'MaxChangeInManipulatedValuePerUnitTime' is the original name of this property."""

        temp = self.wrapped.MaxChangeInManipulatedValuePerUnitTime

        if temp is None:
            return None

        return temp

    @max_change_in_manipulated_value_per_unit_time.setter
    def max_change_in_manipulated_value_per_unit_time(self, value: 'float'):
        self.wrapped.MaxChangeInManipulatedValuePerUnitTime = float(value) if value else 0.0

    @property
    def max_manipulated_value(self) -> 'float':
        """float: 'MaxManipulatedValue' is the original name of this property."""

        temp = self.wrapped.MaxManipulatedValue

        if temp is None:
            return None

        return temp

    @max_manipulated_value.setter
    def max_manipulated_value(self, value: 'float'):
        self.wrapped.MaxManipulatedValue = float(value) if value else 0.0

    @property
    def min_manipulated_value(self) -> 'float':
        """float: 'MinManipulatedValue' is the original name of this property."""

        temp = self.wrapped.MinManipulatedValue

        if temp is None:
            return None

        return temp

    @min_manipulated_value.setter
    def min_manipulated_value(self, value: 'float'):
        self.wrapped.MinManipulatedValue = float(value) if value else 0.0

    @property
    def pid_calculates_change_in_manipulated_value(self) -> 'bool':
        """bool: 'PIDCalculatesChangeInManipulatedValue' is the original name of this property."""

        temp = self.wrapped.PIDCalculatesChangeInManipulatedValue

        if temp is None:
            return None

        return temp

    @pid_calculates_change_in_manipulated_value.setter
    def pid_calculates_change_in_manipulated_value(self, value: 'bool'):
        self.wrapped.PIDCalculatesChangeInManipulatedValue = bool(value) if value else False

    @property
    def proportional_gain(self) -> 'float':
        """float: 'ProportionalGain' is the original name of this property."""

        temp = self.wrapped.ProportionalGain

        if temp is None:
            return None

        return temp

    @proportional_gain.setter
    def proportional_gain(self, value: 'float'):
        self.wrapped.ProportionalGain = float(value) if value else 0.0

    @property
    def proportional_gain_vs_time_and_error(self) -> '_1373.GriddedSurfaceAccessor':
        """GriddedSurfaceAccessor: 'ProportionalGainVsTimeAndError' is the original name of this property."""

        temp = self.wrapped.ProportionalGainVsTimeAndError

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @proportional_gain_vs_time_and_error.setter
    def proportional_gain_vs_time_and_error(self, value: '_1373.GriddedSurfaceAccessor'):
        value = value.wrapped if value else None
        self.wrapped.ProportionalGainVsTimeAndError = value

    @property
    def set_point_value(self) -> 'float':
        """float: 'SetPointValue' is the original name of this property."""

        temp = self.wrapped.SetPointValue

        if temp is None:
            return None

        return temp

    @set_point_value.setter
    def set_point_value(self, value: 'float'):
        self.wrapped.SetPointValue = float(value) if value else 0.0

    @property
    def update_frequency(self) -> 'float':
        """float: 'UpdateFrequency' is the original name of this property."""

        temp = self.wrapped.UpdateFrequency

        if temp is None:
            return None

        return temp

    @update_frequency.setter
    def update_frequency(self, value: 'float'):
        self.wrapped.UpdateFrequency = float(value) if value else 0.0

    @property
    def update_method(self) -> '_1329.PIDControlUpdateMethod':
        """PIDControlUpdateMethod: 'UpdateMethod' is the original name of this property."""

        temp = self.wrapped.UpdateMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1329.PIDControlUpdateMethod)(value) if value is not None else None

    @update_method.setter
    def update_method(self, value: '_1329.PIDControlUpdateMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.UpdateMethod = value

    @property
    def update_time(self) -> 'float':
        """float: 'UpdateTime' is the original name of this property."""

        temp = self.wrapped.UpdateTime

        if temp is None:
            return None

        return temp

    @update_time.setter
    def update_time(self, value: 'float'):
        self.wrapped.UpdateTime = float(value) if value else 0.0

    @property
    def use_differential_gain_scheduling(self) -> 'bool':
        """bool: 'UseDifferentialGainScheduling' is the original name of this property."""

        temp = self.wrapped.UseDifferentialGainScheduling

        if temp is None:
            return None

        return temp

    @use_differential_gain_scheduling.setter
    def use_differential_gain_scheduling(self, value: 'bool'):
        self.wrapped.UseDifferentialGainScheduling = bool(value) if value else False

    @property
    def use_integral_gain_scheduling(self) -> 'bool':
        """bool: 'UseIntegralGainScheduling' is the original name of this property."""

        temp = self.wrapped.UseIntegralGainScheduling

        if temp is None:
            return None

        return temp

    @use_integral_gain_scheduling.setter
    def use_integral_gain_scheduling(self, value: 'bool'):
        self.wrapped.UseIntegralGainScheduling = bool(value) if value else False

    @property
    def use_integrator_anti_windup(self) -> 'bool':
        """bool: 'UseIntegratorAntiWindup' is the original name of this property."""

        temp = self.wrapped.UseIntegratorAntiWindup

        if temp is None:
            return None

        return temp

    @use_integrator_anti_windup.setter
    def use_integrator_anti_windup(self, value: 'bool'):
        self.wrapped.UseIntegratorAntiWindup = bool(value) if value else False

    @property
    def use_proportional_gain_scheduling(self) -> 'bool':
        """bool: 'UseProportionalGainScheduling' is the original name of this property."""

        temp = self.wrapped.UseProportionalGainScheduling

        if temp is None:
            return None

        return temp

    @use_proportional_gain_scheduling.setter
    def use_proportional_gain_scheduling(self, value: 'bool'):
        self.wrapped.UseProportionalGainScheduling = bool(value) if value else False
