"""_1352.py

OptimizationVariable
"""


from typing import List

from mastapy.utility.units_and_measurements import _1406
from mastapy._internal import constructor, conversion
from mastapy.utility.units_and_measurements.measurements import (
    _1413, _1414, _1415, _1416,
    _1417, _1418, _1419, _1420,
    _1421, _1422, _1423, _1424,
    _1425, _1426, _1427, _1428,
    _1429, _1430, _1431, _1432,
    _1433, _1434, _1435, _1436,
    _1437, _1438, _1439, _1440,
    _1441, _1442, _1443, _1444,
    _1445, _1446, _1447, _1448,
    _1449, _1450, _1451, _1452,
    _1453, _1454, _1455, _1456,
    _1457, _1458, _1459, _1460,
    _1461, _1462, _1463, _1464,
    _1465, _1466, _1467, _1468,
    _1469, _1470, _1471, _1472,
    _1473, _1474, _1475, _1476,
    _1477, _1478, _1479, _1480,
    _1481, _1482, _1483, _1484,
    _1485, _1486, _1487, _1488,
    _1489, _1490, _1491, _1492,
    _1493, _1494, _1495, _1496,
    _1497, _1498, _1499, _1500,
    _1501, _1502, _1503, _1504,
    _1505, _1506, _1507, _1508,
    _1509, _1510, _1511, _1512,
    _1513, _1514, _1515, _1516,
    _1517, _1518, _1519, _1520
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_OPTIMIZATION_VARIABLE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'OptimizationVariable')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimizationVariable',)


class OptimizationVariable(_0.APIBase):
    """OptimizationVariable

    This is a mastapy class.
    """

    TYPE = _OPTIMIZATION_VARIABLE

    def __init__(self, instance_to_wrap: 'OptimizationVariable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def measurement(self) -> '_1406.MeasurementBase':
        """MeasurementBase: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1406.MeasurementBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to MeasurementBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement.setter
    def measurement(self, value: '_1406.MeasurementBase'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_acceleration(self) -> '_1413.Acceleration':
        """Acceleration: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1413.Acceleration.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Acceleration. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_acceleration.setter
    def measurement_of_type_acceleration(self, value: '_1413.Acceleration'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angle(self) -> '_1414.Angle':
        """Angle: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1414.Angle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Angle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_angle.setter
    def measurement_of_type_angle(self, value: '_1414.Angle'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angle_per_unit_temperature(self) -> '_1415.AnglePerUnitTemperature':
        """AnglePerUnitTemperature: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1415.AnglePerUnitTemperature.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to AnglePerUnitTemperature. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_angle_per_unit_temperature.setter
    def measurement_of_type_angle_per_unit_temperature(self, value: '_1415.AnglePerUnitTemperature'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angle_small(self) -> '_1416.AngleSmall':
        """AngleSmall: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1416.AngleSmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngleSmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_angle_small.setter
    def measurement_of_type_angle_small(self, value: '_1416.AngleSmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angle_very_small(self) -> '_1417.AngleVerySmall':
        """AngleVerySmall: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1417.AngleVerySmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngleVerySmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_angle_very_small.setter
    def measurement_of_type_angle_very_small(self, value: '_1417.AngleVerySmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angular_acceleration(self) -> '_1418.AngularAcceleration':
        """AngularAcceleration: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1418.AngularAcceleration.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularAcceleration. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_angular_acceleration.setter
    def measurement_of_type_angular_acceleration(self, value: '_1418.AngularAcceleration'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angular_compliance(self) -> '_1419.AngularCompliance':
        """AngularCompliance: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1419.AngularCompliance.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularCompliance. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_angular_compliance.setter
    def measurement_of_type_angular_compliance(self, value: '_1419.AngularCompliance'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angular_jerk(self) -> '_1420.AngularJerk':
        """AngularJerk: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1420.AngularJerk.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularJerk. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_angular_jerk.setter
    def measurement_of_type_angular_jerk(self, value: '_1420.AngularJerk'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angular_stiffness(self) -> '_1421.AngularStiffness':
        """AngularStiffness: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1421.AngularStiffness.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularStiffness. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_angular_stiffness.setter
    def measurement_of_type_angular_stiffness(self, value: '_1421.AngularStiffness'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angular_velocity(self) -> '_1422.AngularVelocity':
        """AngularVelocity: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1422.AngularVelocity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularVelocity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_angular_velocity.setter
    def measurement_of_type_angular_velocity(self, value: '_1422.AngularVelocity'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_area(self) -> '_1423.Area':
        """Area: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1423.Area.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Area. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_area.setter
    def measurement_of_type_area(self, value: '_1423.Area'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_area_small(self) -> '_1424.AreaSmall':
        """AreaSmall: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1424.AreaSmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to AreaSmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_area_small.setter
    def measurement_of_type_area_small(self, value: '_1424.AreaSmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_cycles(self) -> '_1425.Cycles':
        """Cycles: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1425.Cycles.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Cycles. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_cycles.setter
    def measurement_of_type_cycles(self, value: '_1425.Cycles'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_damage(self) -> '_1426.Damage':
        """Damage: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1426.Damage.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Damage. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_damage.setter
    def measurement_of_type_damage(self, value: '_1426.Damage'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_damage_rate(self) -> '_1427.DamageRate':
        """DamageRate: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1427.DamageRate.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to DamageRate. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_damage_rate.setter
    def measurement_of_type_damage_rate(self, value: '_1427.DamageRate'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_data_size(self) -> '_1428.DataSize':
        """DataSize: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1428.DataSize.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to DataSize. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_data_size.setter
    def measurement_of_type_data_size(self, value: '_1428.DataSize'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_decibel(self) -> '_1429.Decibel':
        """Decibel: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1429.Decibel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Decibel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_decibel.setter
    def measurement_of_type_decibel(self, value: '_1429.Decibel'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_density(self) -> '_1430.Density':
        """Density: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1430.Density.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Density. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_density.setter
    def measurement_of_type_density(self, value: '_1430.Density'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_energy(self) -> '_1431.Energy':
        """Energy: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1431.Energy.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Energy. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_energy.setter
    def measurement_of_type_energy(self, value: '_1431.Energy'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_energy_per_unit_area(self) -> '_1432.EnergyPerUnitArea':
        """EnergyPerUnitArea: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1432.EnergyPerUnitArea.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to EnergyPerUnitArea. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_energy_per_unit_area.setter
    def measurement_of_type_energy_per_unit_area(self, value: '_1432.EnergyPerUnitArea'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_energy_per_unit_area_small(self) -> '_1433.EnergyPerUnitAreaSmall':
        """EnergyPerUnitAreaSmall: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1433.EnergyPerUnitAreaSmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to EnergyPerUnitAreaSmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_energy_per_unit_area_small.setter
    def measurement_of_type_energy_per_unit_area_small(self, value: '_1433.EnergyPerUnitAreaSmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_energy_small(self) -> '_1434.EnergySmall':
        """EnergySmall: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1434.EnergySmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to EnergySmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_energy_small.setter
    def measurement_of_type_energy_small(self, value: '_1434.EnergySmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_enum(self) -> '_1435.Enum':
        """Enum: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1435.Enum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Enum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_enum.setter
    def measurement_of_type_enum(self, value: '_1435.Enum'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_flow_rate(self) -> '_1436.FlowRate':
        """FlowRate: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1436.FlowRate.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to FlowRate. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_flow_rate.setter
    def measurement_of_type_flow_rate(self, value: '_1436.FlowRate'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_force(self) -> '_1437.Force':
        """Force: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1437.Force.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Force. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_force.setter
    def measurement_of_type_force(self, value: '_1437.Force'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_force_per_unit_length(self) -> '_1438.ForcePerUnitLength':
        """ForcePerUnitLength: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1438.ForcePerUnitLength.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to ForcePerUnitLength. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_force_per_unit_length.setter
    def measurement_of_type_force_per_unit_length(self, value: '_1438.ForcePerUnitLength'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_force_per_unit_pressure(self) -> '_1439.ForcePerUnitPressure':
        """ForcePerUnitPressure: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1439.ForcePerUnitPressure.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to ForcePerUnitPressure. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_force_per_unit_pressure.setter
    def measurement_of_type_force_per_unit_pressure(self, value: '_1439.ForcePerUnitPressure'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_force_per_unit_temperature(self) -> '_1440.ForcePerUnitTemperature':
        """ForcePerUnitTemperature: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1440.ForcePerUnitTemperature.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to ForcePerUnitTemperature. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_force_per_unit_temperature.setter
    def measurement_of_type_force_per_unit_temperature(self, value: '_1440.ForcePerUnitTemperature'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_fraction_measurement_base(self) -> '_1441.FractionMeasurementBase':
        """FractionMeasurementBase: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1441.FractionMeasurementBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to FractionMeasurementBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_fraction_measurement_base.setter
    def measurement_of_type_fraction_measurement_base(self, value: '_1441.FractionMeasurementBase'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_frequency(self) -> '_1442.Frequency':
        """Frequency: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1442.Frequency.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Frequency. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_frequency.setter
    def measurement_of_type_frequency(self, value: '_1442.Frequency'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_fuel_consumption_engine(self) -> '_1443.FuelConsumptionEngine':
        """FuelConsumptionEngine: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1443.FuelConsumptionEngine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to FuelConsumptionEngine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_fuel_consumption_engine.setter
    def measurement_of_type_fuel_consumption_engine(self, value: '_1443.FuelConsumptionEngine'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_fuel_efficiency_vehicle(self) -> '_1444.FuelEfficiencyVehicle':
        """FuelEfficiencyVehicle: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1444.FuelEfficiencyVehicle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to FuelEfficiencyVehicle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_fuel_efficiency_vehicle.setter
    def measurement_of_type_fuel_efficiency_vehicle(self, value: '_1444.FuelEfficiencyVehicle'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_gradient(self) -> '_1445.Gradient':
        """Gradient: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1445.Gradient.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Gradient. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_gradient.setter
    def measurement_of_type_gradient(self, value: '_1445.Gradient'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_heat_conductivity(self) -> '_1446.HeatConductivity':
        """HeatConductivity: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1446.HeatConductivity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatConductivity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_heat_conductivity.setter
    def measurement_of_type_heat_conductivity(self, value: '_1446.HeatConductivity'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_heat_transfer(self) -> '_1447.HeatTransfer':
        """HeatTransfer: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1447.HeatTransfer.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatTransfer. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_heat_transfer.setter
    def measurement_of_type_heat_transfer(self, value: '_1447.HeatTransfer'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self) -> '_1448.HeatTransferCoefficientForPlasticGearTooth':
        """HeatTransferCoefficientForPlasticGearTooth: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1448.HeatTransferCoefficientForPlasticGearTooth.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatTransferCoefficientForPlasticGearTooth. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_heat_transfer_coefficient_for_plastic_gear_tooth.setter
    def measurement_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self, value: '_1448.HeatTransferCoefficientForPlasticGearTooth'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_heat_transfer_resistance(self) -> '_1449.HeatTransferResistance':
        """HeatTransferResistance: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1449.HeatTransferResistance.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatTransferResistance. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_heat_transfer_resistance.setter
    def measurement_of_type_heat_transfer_resistance(self, value: '_1449.HeatTransferResistance'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_impulse(self) -> '_1450.Impulse':
        """Impulse: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1450.Impulse.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Impulse. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_impulse.setter
    def measurement_of_type_impulse(self, value: '_1450.Impulse'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_index(self) -> '_1451.Index':
        """Index: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1451.Index.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Index. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_index.setter
    def measurement_of_type_index(self, value: '_1451.Index'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_integer(self) -> '_1452.Integer':
        """Integer: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1452.Integer.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Integer. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_integer.setter
    def measurement_of_type_integer(self, value: '_1452.Integer'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_inverse_short_length(self) -> '_1453.InverseShortLength':
        """InverseShortLength: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1453.InverseShortLength.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to InverseShortLength. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_inverse_short_length.setter
    def measurement_of_type_inverse_short_length(self, value: '_1453.InverseShortLength'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_inverse_short_time(self) -> '_1454.InverseShortTime':
        """InverseShortTime: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1454.InverseShortTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to InverseShortTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_inverse_short_time.setter
    def measurement_of_type_inverse_short_time(self, value: '_1454.InverseShortTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_jerk(self) -> '_1455.Jerk':
        """Jerk: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1455.Jerk.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Jerk. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_jerk.setter
    def measurement_of_type_jerk(self, value: '_1455.Jerk'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_kinematic_viscosity(self) -> '_1456.KinematicViscosity':
        """KinematicViscosity: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1456.KinematicViscosity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to KinematicViscosity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_kinematic_viscosity.setter
    def measurement_of_type_kinematic_viscosity(self, value: '_1456.KinematicViscosity'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_long(self) -> '_1457.LengthLong':
        """LengthLong: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1457.LengthLong.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthLong. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_length_long.setter
    def measurement_of_type_length_long(self, value: '_1457.LengthLong'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_medium(self) -> '_1458.LengthMedium':
        """LengthMedium: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1458.LengthMedium.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthMedium. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_length_medium.setter
    def measurement_of_type_length_medium(self, value: '_1458.LengthMedium'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_per_unit_temperature(self) -> '_1459.LengthPerUnitTemperature':
        """LengthPerUnitTemperature: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1459.LengthPerUnitTemperature.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthPerUnitTemperature. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_length_per_unit_temperature.setter
    def measurement_of_type_length_per_unit_temperature(self, value: '_1459.LengthPerUnitTemperature'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_short(self) -> '_1460.LengthShort':
        """LengthShort: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1460.LengthShort.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthShort. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_length_short.setter
    def measurement_of_type_length_short(self, value: '_1460.LengthShort'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_to_the_fourth(self) -> '_1461.LengthToTheFourth':
        """LengthToTheFourth: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1461.LengthToTheFourth.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthToTheFourth. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_length_to_the_fourth.setter
    def measurement_of_type_length_to_the_fourth(self, value: '_1461.LengthToTheFourth'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_very_long(self) -> '_1462.LengthVeryLong':
        """LengthVeryLong: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1462.LengthVeryLong.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthVeryLong. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_length_very_long.setter
    def measurement_of_type_length_very_long(self, value: '_1462.LengthVeryLong'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_very_short(self) -> '_1463.LengthVeryShort':
        """LengthVeryShort: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1463.LengthVeryShort.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthVeryShort. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_length_very_short.setter
    def measurement_of_type_length_very_short(self, value: '_1463.LengthVeryShort'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_very_short_per_length_short(self) -> '_1464.LengthVeryShortPerLengthShort':
        """LengthVeryShortPerLengthShort: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1464.LengthVeryShortPerLengthShort.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthVeryShortPerLengthShort. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_length_very_short_per_length_short.setter
    def measurement_of_type_length_very_short_per_length_short(self, value: '_1464.LengthVeryShortPerLengthShort'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_linear_angular_damping(self) -> '_1465.LinearAngularDamping':
        """LinearAngularDamping: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1465.LinearAngularDamping.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearAngularDamping. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_linear_angular_damping.setter
    def measurement_of_type_linear_angular_damping(self, value: '_1465.LinearAngularDamping'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_linear_angular_stiffness_cross_term(self) -> '_1466.LinearAngularStiffnessCrossTerm':
        """LinearAngularStiffnessCrossTerm: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1466.LinearAngularStiffnessCrossTerm.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearAngularStiffnessCrossTerm. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_linear_angular_stiffness_cross_term.setter
    def measurement_of_type_linear_angular_stiffness_cross_term(self, value: '_1466.LinearAngularStiffnessCrossTerm'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_linear_damping(self) -> '_1467.LinearDamping':
        """LinearDamping: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1467.LinearDamping.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearDamping. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_linear_damping.setter
    def measurement_of_type_linear_damping(self, value: '_1467.LinearDamping'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_linear_flexibility(self) -> '_1468.LinearFlexibility':
        """LinearFlexibility: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1468.LinearFlexibility.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearFlexibility. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_linear_flexibility.setter
    def measurement_of_type_linear_flexibility(self, value: '_1468.LinearFlexibility'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_linear_stiffness(self) -> '_1469.LinearStiffness':
        """LinearStiffness: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1469.LinearStiffness.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearStiffness. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_linear_stiffness.setter
    def measurement_of_type_linear_stiffness(self, value: '_1469.LinearStiffness'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_mass(self) -> '_1470.Mass':
        """Mass: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1470.Mass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Mass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_mass.setter
    def measurement_of_type_mass(self, value: '_1470.Mass'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_mass_per_unit_length(self) -> '_1471.MassPerUnitLength':
        """MassPerUnitLength: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1471.MassPerUnitLength.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to MassPerUnitLength. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_mass_per_unit_length.setter
    def measurement_of_type_mass_per_unit_length(self, value: '_1471.MassPerUnitLength'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_mass_per_unit_time(self) -> '_1472.MassPerUnitTime':
        """MassPerUnitTime: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1472.MassPerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to MassPerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_mass_per_unit_time.setter
    def measurement_of_type_mass_per_unit_time(self, value: '_1472.MassPerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_moment_of_inertia(self) -> '_1473.MomentOfInertia':
        """MomentOfInertia: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1473.MomentOfInertia.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to MomentOfInertia. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_moment_of_inertia.setter
    def measurement_of_type_moment_of_inertia(self, value: '_1473.MomentOfInertia'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_moment_of_inertia_per_unit_length(self) -> '_1474.MomentOfInertiaPerUnitLength':
        """MomentOfInertiaPerUnitLength: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1474.MomentOfInertiaPerUnitLength.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to MomentOfInertiaPerUnitLength. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_moment_of_inertia_per_unit_length.setter
    def measurement_of_type_moment_of_inertia_per_unit_length(self, value: '_1474.MomentOfInertiaPerUnitLength'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_moment_per_unit_pressure(self) -> '_1475.MomentPerUnitPressure':
        """MomentPerUnitPressure: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1475.MomentPerUnitPressure.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to MomentPerUnitPressure. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_moment_per_unit_pressure.setter
    def measurement_of_type_moment_per_unit_pressure(self, value: '_1475.MomentPerUnitPressure'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_number(self) -> '_1476.Number':
        """Number: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1476.Number.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Number. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_number.setter
    def measurement_of_type_number(self, value: '_1476.Number'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_percentage(self) -> '_1477.Percentage':
        """Percentage: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1477.Percentage.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Percentage. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_percentage.setter
    def measurement_of_type_percentage(self, value: '_1477.Percentage'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power(self) -> '_1478.Power':
        """Power: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1478.Power.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Power. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_power.setter
    def measurement_of_type_power(self, value: '_1478.Power'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_per_small_area(self) -> '_1479.PowerPerSmallArea':
        """PowerPerSmallArea: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1479.PowerPerSmallArea.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerPerSmallArea. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_power_per_small_area.setter
    def measurement_of_type_power_per_small_area(self, value: '_1479.PowerPerSmallArea'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_per_unit_time(self) -> '_1480.PowerPerUnitTime':
        """PowerPerUnitTime: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1480.PowerPerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerPerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_power_per_unit_time.setter
    def measurement_of_type_power_per_unit_time(self, value: '_1480.PowerPerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_small(self) -> '_1481.PowerSmall':
        """PowerSmall: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1481.PowerSmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_power_small.setter
    def measurement_of_type_power_small(self, value: '_1481.PowerSmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_small_per_area(self) -> '_1482.PowerSmallPerArea':
        """PowerSmallPerArea: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1482.PowerSmallPerArea.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmallPerArea. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_power_small_per_area.setter
    def measurement_of_type_power_small_per_area(self, value: '_1482.PowerSmallPerArea'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_small_per_unit_area_per_unit_time(self) -> '_1483.PowerSmallPerUnitAreaPerUnitTime':
        """PowerSmallPerUnitAreaPerUnitTime: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1483.PowerSmallPerUnitAreaPerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmallPerUnitAreaPerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_power_small_per_unit_area_per_unit_time.setter
    def measurement_of_type_power_small_per_unit_area_per_unit_time(self, value: '_1483.PowerSmallPerUnitAreaPerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_small_per_unit_time(self) -> '_1484.PowerSmallPerUnitTime':
        """PowerSmallPerUnitTime: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1484.PowerSmallPerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmallPerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_power_small_per_unit_time.setter
    def measurement_of_type_power_small_per_unit_time(self, value: '_1484.PowerSmallPerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_pressure(self) -> '_1485.Pressure':
        """Pressure: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1485.Pressure.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Pressure. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_pressure.setter
    def measurement_of_type_pressure(self, value: '_1485.Pressure'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_pressure_per_unit_time(self) -> '_1486.PressurePerUnitTime':
        """PressurePerUnitTime: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1486.PressurePerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to PressurePerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_pressure_per_unit_time.setter
    def measurement_of_type_pressure_per_unit_time(self, value: '_1486.PressurePerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_pressure_velocity_product(self) -> '_1487.PressureVelocityProduct':
        """PressureVelocityProduct: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1487.PressureVelocityProduct.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to PressureVelocityProduct. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_pressure_velocity_product.setter
    def measurement_of_type_pressure_velocity_product(self, value: '_1487.PressureVelocityProduct'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_pressure_viscosity_coefficient(self) -> '_1488.PressureViscosityCoefficient':
        """PressureViscosityCoefficient: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1488.PressureViscosityCoefficient.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to PressureViscosityCoefficient. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_pressure_viscosity_coefficient.setter
    def measurement_of_type_pressure_viscosity_coefficient(self, value: '_1488.PressureViscosityCoefficient'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_price(self) -> '_1489.Price':
        """Price: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1489.Price.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Price. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_price.setter
    def measurement_of_type_price(self, value: '_1489.Price'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_quadratic_angular_damping(self) -> '_1490.QuadraticAngularDamping':
        """QuadraticAngularDamping: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1490.QuadraticAngularDamping.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to QuadraticAngularDamping. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_quadratic_angular_damping.setter
    def measurement_of_type_quadratic_angular_damping(self, value: '_1490.QuadraticAngularDamping'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_quadratic_drag(self) -> '_1491.QuadraticDrag':
        """QuadraticDrag: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1491.QuadraticDrag.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to QuadraticDrag. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_quadratic_drag.setter
    def measurement_of_type_quadratic_drag(self, value: '_1491.QuadraticDrag'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_rescaled_measurement(self) -> '_1492.RescaledMeasurement':
        """RescaledMeasurement: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1492.RescaledMeasurement.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to RescaledMeasurement. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_rescaled_measurement.setter
    def measurement_of_type_rescaled_measurement(self, value: '_1492.RescaledMeasurement'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_rotatum(self) -> '_1493.Rotatum':
        """Rotatum: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1493.Rotatum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Rotatum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_rotatum.setter
    def measurement_of_type_rotatum(self, value: '_1493.Rotatum'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_safety_factor(self) -> '_1494.SafetyFactor':
        """SafetyFactor: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1494.SafetyFactor.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to SafetyFactor. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_safety_factor.setter
    def measurement_of_type_safety_factor(self, value: '_1494.SafetyFactor'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_specific_acoustic_impedance(self) -> '_1495.SpecificAcousticImpedance':
        """SpecificAcousticImpedance: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1495.SpecificAcousticImpedance.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to SpecificAcousticImpedance. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_specific_acoustic_impedance.setter
    def measurement_of_type_specific_acoustic_impedance(self, value: '_1495.SpecificAcousticImpedance'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_specific_heat(self) -> '_1496.SpecificHeat':
        """SpecificHeat: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1496.SpecificHeat.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to SpecificHeat. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_specific_heat.setter
    def measurement_of_type_specific_heat(self, value: '_1496.SpecificHeat'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_square_root_of_unit_force_per_unit_area(self) -> '_1497.SquareRootOfUnitForcePerUnitArea':
        """SquareRootOfUnitForcePerUnitArea: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1497.SquareRootOfUnitForcePerUnitArea.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to SquareRootOfUnitForcePerUnitArea. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_square_root_of_unit_force_per_unit_area.setter
    def measurement_of_type_square_root_of_unit_force_per_unit_area(self, value: '_1497.SquareRootOfUnitForcePerUnitArea'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_stiffness_per_unit_face_width(self) -> '_1498.StiffnessPerUnitFaceWidth':
        """StiffnessPerUnitFaceWidth: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1498.StiffnessPerUnitFaceWidth.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to StiffnessPerUnitFaceWidth. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_stiffness_per_unit_face_width.setter
    def measurement_of_type_stiffness_per_unit_face_width(self, value: '_1498.StiffnessPerUnitFaceWidth'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_stress(self) -> '_1499.Stress':
        """Stress: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1499.Stress.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Stress. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_stress.setter
    def measurement_of_type_stress(self, value: '_1499.Stress'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_temperature(self) -> '_1500.Temperature':
        """Temperature: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1500.Temperature.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Temperature. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_temperature.setter
    def measurement_of_type_temperature(self, value: '_1500.Temperature'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_temperature_difference(self) -> '_1501.TemperatureDifference':
        """TemperatureDifference: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1501.TemperatureDifference.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to TemperatureDifference. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_temperature_difference.setter
    def measurement_of_type_temperature_difference(self, value: '_1501.TemperatureDifference'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_temperature_per_unit_time(self) -> '_1502.TemperaturePerUnitTime':
        """TemperaturePerUnitTime: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1502.TemperaturePerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to TemperaturePerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_temperature_per_unit_time.setter
    def measurement_of_type_temperature_per_unit_time(self, value: '_1502.TemperaturePerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_text(self) -> '_1503.Text':
        """Text: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1503.Text.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Text. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_text.setter
    def measurement_of_type_text(self, value: '_1503.Text'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_thermal_contact_coefficient(self) -> '_1504.ThermalContactCoefficient':
        """ThermalContactCoefficient: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1504.ThermalContactCoefficient.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to ThermalContactCoefficient. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_thermal_contact_coefficient.setter
    def measurement_of_type_thermal_contact_coefficient(self, value: '_1504.ThermalContactCoefficient'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_thermal_expansion_coefficient(self) -> '_1505.ThermalExpansionCoefficient':
        """ThermalExpansionCoefficient: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1505.ThermalExpansionCoefficient.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to ThermalExpansionCoefficient. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_thermal_expansion_coefficient.setter
    def measurement_of_type_thermal_expansion_coefficient(self, value: '_1505.ThermalExpansionCoefficient'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_thermo_elastic_factor(self) -> '_1506.ThermoElasticFactor':
        """ThermoElasticFactor: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1506.ThermoElasticFactor.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to ThermoElasticFactor. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_thermo_elastic_factor.setter
    def measurement_of_type_thermo_elastic_factor(self, value: '_1506.ThermoElasticFactor'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_time(self) -> '_1507.Time':
        """Time: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1507.Time.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Time. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_time.setter
    def measurement_of_type_time(self, value: '_1507.Time'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_time_short(self) -> '_1508.TimeShort':
        """TimeShort: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1508.TimeShort.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to TimeShort. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_time_short.setter
    def measurement_of_type_time_short(self, value: '_1508.TimeShort'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_time_very_short(self) -> '_1509.TimeVeryShort':
        """TimeVeryShort: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1509.TimeVeryShort.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to TimeVeryShort. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_time_very_short.setter
    def measurement_of_type_time_very_short(self, value: '_1509.TimeVeryShort'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_torque(self) -> '_1510.Torque':
        """Torque: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1510.Torque.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Torque. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_torque.setter
    def measurement_of_type_torque(self, value: '_1510.Torque'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_torque_converter_inverse_k(self) -> '_1511.TorqueConverterInverseK':
        """TorqueConverterInverseK: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1511.TorqueConverterInverseK.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to TorqueConverterInverseK. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_torque_converter_inverse_k.setter
    def measurement_of_type_torque_converter_inverse_k(self, value: '_1511.TorqueConverterInverseK'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_torque_converter_k(self) -> '_1512.TorqueConverterK':
        """TorqueConverterK: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1512.TorqueConverterK.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to TorqueConverterK. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_torque_converter_k.setter
    def measurement_of_type_torque_converter_k(self, value: '_1512.TorqueConverterK'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_torque_per_unit_temperature(self) -> '_1513.TorquePerUnitTemperature':
        """TorquePerUnitTemperature: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1513.TorquePerUnitTemperature.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to TorquePerUnitTemperature. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_torque_per_unit_temperature.setter
    def measurement_of_type_torque_per_unit_temperature(self, value: '_1513.TorquePerUnitTemperature'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_velocity(self) -> '_1514.Velocity':
        """Velocity: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1514.Velocity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Velocity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_velocity.setter
    def measurement_of_type_velocity(self, value: '_1514.Velocity'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_velocity_small(self) -> '_1515.VelocitySmall':
        """VelocitySmall: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1515.VelocitySmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to VelocitySmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_velocity_small.setter
    def measurement_of_type_velocity_small(self, value: '_1515.VelocitySmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_viscosity(self) -> '_1516.Viscosity':
        """Viscosity: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1516.Viscosity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Viscosity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_viscosity.setter
    def measurement_of_type_viscosity(self, value: '_1516.Viscosity'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_voltage(self) -> '_1517.Voltage':
        """Voltage: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1517.Voltage.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Voltage. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_voltage.setter
    def measurement_of_type_voltage(self, value: '_1517.Voltage'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_volume(self) -> '_1518.Volume':
        """Volume: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1518.Volume.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Volume. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_volume.setter
    def measurement_of_type_volume(self, value: '_1518.Volume'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_wear_coefficient(self) -> '_1519.WearCoefficient':
        """WearCoefficient: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1519.WearCoefficient.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to WearCoefficient. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_wear_coefficient.setter
    def measurement_of_type_wear_coefficient(self, value: '_1519.WearCoefficient'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_yank(self) -> '_1520.Yank':
        """Yank: 'Measurement' is the original name of this property."""

        temp = self.wrapped.Measurement

        if temp is None:
            return None

        if _1520.Yank.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast measurement to Yank. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measurement_of_type_yank.setter
    def measurement_of_type_yank(self, value: '_1520.Yank'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def results(self) -> 'List[float]':
        """List[float]: 'Results' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Results

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)
        return value
