"""_5216.py

RootAssemblyMultibodyDynamicsAnalysis
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model import _2224
from mastapy.system_model.analyses_and_results.mbd_analyses import _2388, _5119
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'RootAssemblyMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyMultibodyDynamicsAnalysis',)


class RootAssemblyMultibodyDynamicsAnalysis(_5119.AssemblyMultibodyDynamicsAnalysis):
    """RootAssemblyMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'RootAssemblyMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def actual_torque_ratio(self) -> 'float':
        """float: 'ActualTorqueRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActualTorqueRatio

        if temp is None:
            return None

        return temp

    @property
    def actual_torque_ratio_turbine_to_output(self) -> 'float':
        """float: 'ActualTorqueRatioTurbineToOutput' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActualTorqueRatioTurbineToOutput

        if temp is None:
            return None

        return temp

    @property
    def brake_force(self) -> 'float':
        """float: 'BrakeForce' is the original name of this property."""

        temp = self.wrapped.BrakeForce

        if temp is None:
            return None

        return temp

    @brake_force.setter
    def brake_force(self, value: 'float'):
        self.wrapped.BrakeForce = float(value) if value else 0.0

    @property
    def current_target_vehicle_speed(self) -> 'float':
        """float: 'CurrentTargetVehicleSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentTargetVehicleSpeed

        if temp is None:
            return None

        return temp

    @property
    def efficiency(self) -> 'float':
        """float: 'Efficiency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Efficiency

        if temp is None:
            return None

        return temp

    @property
    def energy_lost(self) -> 'float':
        """float: 'EnergyLost' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EnergyLost

        if temp is None:
            return None

        return temp

    @property
    def force_from_road_incline(self) -> 'float':
        """float: 'ForceFromRoadIncline' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceFromRoadIncline

        if temp is None:
            return None

        return temp

    @property
    def force_from_wheels(self) -> 'float':
        """float: 'ForceFromWheels' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceFromWheels

        if temp is None:
            return None

        return temp

    @property
    def input_energy(self) -> 'float':
        """float: 'InputEnergy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InputEnergy

        if temp is None:
            return None

        return temp

    @property
    def input_power(self) -> 'float':
        """float: 'InputPower' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InputPower

        if temp is None:
            return None

        return temp

    @property
    def log_10_time_step(self) -> 'float':
        """float: 'Log10TimeStep' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Log10TimeStep

        if temp is None:
            return None

        return temp

    @property
    def maximum_vehicle_speed_error(self) -> 'float':
        """float: 'MaximumVehicleSpeedError' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumVehicleSpeedError

        if temp is None:
            return None

        return temp

    @property
    def oil_dynamic_temperature(self) -> 'float':
        """float: 'OilDynamicTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OilDynamicTemperature

        if temp is None:
            return None

        return temp

    @property
    def overall_efficiency(self) -> 'float':
        """float: 'OverallEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverallEfficiency

        if temp is None:
            return None

        return temp

    @property
    def percentage_error_in_vehicle_speed_compared_to_drive_cycle(self) -> 'float':
        """float: 'PercentageErrorInVehicleSpeedComparedToDriveCycle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PercentageErrorInVehicleSpeedComparedToDriveCycle

        if temp is None:
            return None

        return temp

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
    def road_incline(self) -> 'float':
        """float: 'RoadIncline' is the original name of this property."""

        temp = self.wrapped.RoadIncline

        if temp is None:
            return None

        return temp

    @road_incline.setter
    def road_incline(self, value: 'float'):
        self.wrapped.RoadIncline = float(value) if value else 0.0

    @property
    def total_force_on_vehicle(self) -> 'float':
        """float: 'TotalForceOnVehicle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalForceOnVehicle

        if temp is None:
            return None

        return temp

    @property
    def vehicle_acceleration(self) -> 'float':
        """float: 'VehicleAcceleration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VehicleAcceleration

        if temp is None:
            return None

        return temp

    @property
    def vehicle_drag(self) -> 'float':
        """float: 'VehicleDrag' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VehicleDrag

        if temp is None:
            return None

        return temp

    @property
    def vehicle_position(self) -> 'float':
        """float: 'VehiclePosition' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VehiclePosition

        if temp is None:
            return None

        return temp

    @property
    def vehicle_speed(self) -> 'float':
        """float: 'VehicleSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VehicleSpeed

        if temp is None:
            return None

        return temp

    @property
    def vehicle_speed_drive_cycle_error(self) -> 'float':
        """float: 'VehicleSpeedDriveCycleError' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VehicleSpeedDriveCycleError

        if temp is None:
            return None

        return temp

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
    def multibody_dynamics_analysis_inputs(self) -> '_2388.MultibodyDynamicsAnalysis':
        """MultibodyDynamicsAnalysis: 'MultibodyDynamicsAnalysisInputs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MultibodyDynamicsAnalysisInputs

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
