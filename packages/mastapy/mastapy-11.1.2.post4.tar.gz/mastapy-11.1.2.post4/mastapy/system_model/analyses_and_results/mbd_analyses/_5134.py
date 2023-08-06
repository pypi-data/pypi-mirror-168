"""_5134.py

ClutchConnectionMultibodyDynamicsAnalysis
"""


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.couplings import _2093
from mastapy.system_model.analyses_and_results.static_loads import _6556
from mastapy.system_model.analyses_and_results.mbd_analyses import _5151
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ClutchConnectionMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionMultibodyDynamicsAnalysis',)


class ClutchConnectionMultibodyDynamicsAnalysis(_5151.CouplingConnectionMultibodyDynamicsAnalysis):
    """ClutchConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _CLUTCH_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'ClutchConnectionMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def applied_clutch_pressure_at_clutch_plate(self) -> 'float':
        """float: 'AppliedClutchPressureAtClutchPlate' is the original name of this property."""

        temp = self.wrapped.AppliedClutchPressureAtClutchPlate

        if temp is None:
            return None

        return temp

    @applied_clutch_pressure_at_clutch_plate.setter
    def applied_clutch_pressure_at_clutch_plate(self, value: 'float'):
        self.wrapped.AppliedClutchPressureAtClutchPlate = float(value) if value else 0.0

    @property
    def applied_clutch_pressure_at_piston(self) -> 'float':
        """float: 'AppliedClutchPressureAtPiston' is the original name of this property."""

        temp = self.wrapped.AppliedClutchPressureAtPiston

        if temp is None:
            return None

        return temp

    @applied_clutch_pressure_at_piston.setter
    def applied_clutch_pressure_at_piston(self, value: 'float'):
        self.wrapped.AppliedClutchPressureAtPiston = float(value) if value else 0.0

    @property
    def clutch_connection_elastic_torque(self) -> 'float':
        """float: 'ClutchConnectionElasticTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClutchConnectionElasticTorque

        if temp is None:
            return None

        return temp

    @property
    def clutch_connection_viscous_torque(self) -> 'float':
        """float: 'ClutchConnectionViscousTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClutchConnectionViscousTorque

        if temp is None:
            return None

        return temp

    @property
    def clutch_plate_dynamic_temperature(self) -> 'float':
        """float: 'ClutchPlateDynamicTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClutchPlateDynamicTemperature

        if temp is None:
            return None

        return temp

    @property
    def clutch_torque_capacity(self) -> 'float':
        """float: 'ClutchTorqueCapacity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClutchTorqueCapacity

        if temp is None:
            return None

        return temp

    @property
    def excess_clutch_torque_capacity(self) -> 'float':
        """float: 'ExcessClutchTorqueCapacity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcessClutchTorqueCapacity

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
    def relative_shaft_displacement(self) -> 'float':
        """float: 'RelativeShaftDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeShaftDisplacement

        if temp is None:
            return None

        return temp

    @property
    def relative_shaft_speed(self) -> 'float':
        """float: 'RelativeShaftSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeShaftSpeed

        if temp is None:
            return None

        return temp

    @property
    def connection_design(self) -> '_2093.ClutchConnection':
        """ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6556.ClutchConnectionLoadCase':
        """ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
