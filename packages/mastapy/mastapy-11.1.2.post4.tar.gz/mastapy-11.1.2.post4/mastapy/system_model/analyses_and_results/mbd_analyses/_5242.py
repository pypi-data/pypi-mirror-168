"""_5242.py

TorqueConverterConnectionMultibodyDynamicsAnalysis
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5246, _5151
from mastapy.system_model.connections_and_sockets.couplings import _2103
from mastapy.system_model.analyses_and_results.static_loads import _6700
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'TorqueConverterConnectionMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionMultibodyDynamicsAnalysis',)


class TorqueConverterConnectionMultibodyDynamicsAnalysis(_5151.CouplingConnectionMultibodyDynamicsAnalysis):
    """TorqueConverterConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def capacity_factor_k(self) -> 'float':
        """float: 'CapacityFactorK' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CapacityFactorK

        if temp is None:
            return None

        return temp

    @property
    def inverse_capacity_factor_1k(self) -> 'float':
        """float: 'InverseCapacityFactor1K' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InverseCapacityFactor1K

        if temp is None:
            return None

        return temp

    @property
    def is_locked(self) -> 'bool':
        """bool: 'IsLocked' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsLocked

        if temp is None:
            return None

        return temp

    @property
    def lock_up_clutch_temperature(self) -> 'float':
        """float: 'LockUpClutchTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LockUpClutchTemperature

        if temp is None:
            return None

        return temp

    @property
    def lock_up_viscous_torque(self) -> 'float':
        """float: 'LockUpViscousTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LockUpViscousTorque

        if temp is None:
            return None

        return temp

    @property
    def locked_torque(self) -> 'float':
        """float: 'LockedTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LockedTorque

        if temp is None:
            return None

        return temp

    @property
    def locking_status(self) -> '_5246.TorqueConverterStatus':
        """TorqueConverterStatus: 'LockingStatus' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LockingStatus

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5246.TorqueConverterStatus)(value) if value is not None else None

    @property
    def percentage_applied_pressure(self) -> 'float':
        """float: 'PercentageAppliedPressure' is the original name of this property."""

        temp = self.wrapped.PercentageAppliedPressure

        if temp is None:
            return None

        return temp

    @percentage_applied_pressure.setter
    def percentage_applied_pressure(self, value: 'float'):
        self.wrapped.PercentageAppliedPressure = float(value) if value else 0.0

    @property
    def power_loss(self) -> 'float':
        """float: 'PowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoss

        if temp is None:
            return None

        return temp

    @property
    def pump_torque(self) -> 'float':
        """float: 'PumpTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PumpTorque

        if temp is None:
            return None

        return temp

    @property
    def speed_ratio(self) -> 'float':
        """float: 'SpeedRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpeedRatio

        if temp is None:
            return None

        return temp

    @property
    def torque_ratio(self) -> 'float':
        """float: 'TorqueRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueRatio

        if temp is None:
            return None

        return temp

    @property
    def turbine_torque(self) -> 'float':
        """float: 'TurbineTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TurbineTorque

        if temp is None:
            return None

        return temp

    @property
    def connection_design(self) -> '_2103.TorqueConverterConnection':
        """TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6700.TorqueConverterConnectionLoadCase':
        """TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
