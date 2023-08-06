"""_1407.py

MeasurementSettings
"""


from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item, overridable
from mastapy.utility.units_and_measurements import _1406
from mastapy._internal.overridable_constructor import _unpack_overridable
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
from mastapy.units_and_measurements import _7286
from mastapy.utility import _1395
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_SETTINGS = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements', 'MeasurementSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementSettings',)


class MeasurementSettings(_1395.PerMachineSettings):
    """MeasurementSettings

    This is a mastapy class.
    """

    TYPE = _MEASUREMENT_SETTINGS

    def __init__(self, instance_to_wrap: 'MeasurementSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def large_number_cutoff(self) -> 'float':
        """float: 'LargeNumberCutoff' is the original name of this property."""

        temp = self.wrapped.LargeNumberCutoff

        if temp is None:
            return None

        return temp

    @large_number_cutoff.setter
    def large_number_cutoff(self, value: 'float'):
        self.wrapped.LargeNumberCutoff = float(value) if value else 0.0

    @property
    def number_decimal_separator(self) -> 'str':
        """str: 'NumberDecimalSeparator' is the original name of this property."""

        temp = self.wrapped.NumberDecimalSeparator

        if temp is None:
            return None

        return temp

    @number_decimal_separator.setter
    def number_decimal_separator(self, value: 'str'):
        self.wrapped.NumberDecimalSeparator = str(value) if value else ''

    @property
    def number_group_separator(self) -> 'str':
        """str: 'NumberGroupSeparator' is the original name of this property."""

        temp = self.wrapped.NumberGroupSeparator

        if temp is None:
            return None

        return temp

    @number_group_separator.setter
    def number_group_separator(self, value: 'str'):
        self.wrapped.NumberGroupSeparator = str(value) if value else ''

    @property
    def sample_input(self) -> 'str':
        """str: 'SampleInput' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SampleInput

        if temp is None:
            return None

        return temp

    @property
    def sample_output(self) -> 'str':
        """str: 'SampleOutput' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SampleOutput

        if temp is None:
            return None

        return temp

    @property
    def selected_measurement(self) -> 'list_with_selected_item.ListWithSelectedItem_MeasurementBase':
        """list_with_selected_item.ListWithSelectedItem_MeasurementBase: 'SelectedMeasurement' is the original name of this property."""

        temp = self.wrapped.SelectedMeasurement

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_MeasurementBase)(temp) if temp is not None else None

    @selected_measurement.setter
    def selected_measurement(self, value: 'list_with_selected_item.ListWithSelectedItem_MeasurementBase.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_MeasurementBase.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_MeasurementBase.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.SelectedMeasurement = value

    @property
    def show_trailing_zeros(self) -> 'bool':
        """bool: 'ShowTrailingZeros' is the original name of this property."""

        temp = self.wrapped.ShowTrailingZeros

        if temp is None:
            return None

        return temp

    @show_trailing_zeros.setter
    def show_trailing_zeros(self, value: 'bool'):
        self.wrapped.ShowTrailingZeros = bool(value) if value else False

    @property
    def small_number_cutoff(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SmallNumberCutoff' is the original name of this property."""

        temp = self.wrapped.SmallNumberCutoff

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @small_number_cutoff.setter
    def small_number_cutoff(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SmallNumberCutoff = value

    @property
    def current_selected_measurement(self) -> '_1406.MeasurementBase':
        """MeasurementBase: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1406.MeasurementBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MeasurementBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_acceleration(self) -> '_1413.Acceleration':
        """Acceleration: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1413.Acceleration.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Acceleration. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_angle(self) -> '_1414.Angle':
        """Angle: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1414.Angle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Angle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_angle_per_unit_temperature(self) -> '_1415.AnglePerUnitTemperature':
        """AnglePerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1415.AnglePerUnitTemperature.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AnglePerUnitTemperature. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_angle_small(self) -> '_1416.AngleSmall':
        """AngleSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1416.AngleSmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngleSmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_angle_very_small(self) -> '_1417.AngleVerySmall':
        """AngleVerySmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1417.AngleVerySmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngleVerySmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_angular_acceleration(self) -> '_1418.AngularAcceleration':
        """AngularAcceleration: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1418.AngularAcceleration.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularAcceleration. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_angular_compliance(self) -> '_1419.AngularCompliance':
        """AngularCompliance: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1419.AngularCompliance.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularCompliance. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_angular_jerk(self) -> '_1420.AngularJerk':
        """AngularJerk: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1420.AngularJerk.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularJerk. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_angular_stiffness(self) -> '_1421.AngularStiffness':
        """AngularStiffness: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1421.AngularStiffness.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularStiffness. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_angular_velocity(self) -> '_1422.AngularVelocity':
        """AngularVelocity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1422.AngularVelocity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularVelocity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_area(self) -> '_1423.Area':
        """Area: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1423.Area.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Area. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_area_small(self) -> '_1424.AreaSmall':
        """AreaSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1424.AreaSmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AreaSmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_cycles(self) -> '_1425.Cycles':
        """Cycles: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1425.Cycles.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Cycles. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_damage(self) -> '_1426.Damage':
        """Damage: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1426.Damage.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Damage. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_damage_rate(self) -> '_1427.DamageRate':
        """DamageRate: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1427.DamageRate.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to DamageRate. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_data_size(self) -> '_1428.DataSize':
        """DataSize: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1428.DataSize.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to DataSize. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_decibel(self) -> '_1429.Decibel':
        """Decibel: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1429.Decibel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Decibel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_density(self) -> '_1430.Density':
        """Density: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1430.Density.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Density. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_energy(self) -> '_1431.Energy':
        """Energy: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1431.Energy.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Energy. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_energy_per_unit_area(self) -> '_1432.EnergyPerUnitArea':
        """EnergyPerUnitArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1432.EnergyPerUnitArea.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to EnergyPerUnitArea. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_energy_per_unit_area_small(self) -> '_1433.EnergyPerUnitAreaSmall':
        """EnergyPerUnitAreaSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1433.EnergyPerUnitAreaSmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to EnergyPerUnitAreaSmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_energy_small(self) -> '_1434.EnergySmall':
        """EnergySmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1434.EnergySmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to EnergySmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_enum(self) -> '_1435.Enum':
        """Enum: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1435.Enum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Enum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_flow_rate(self) -> '_1436.FlowRate':
        """FlowRate: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1436.FlowRate.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FlowRate. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_force(self) -> '_1437.Force':
        """Force: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1437.Force.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Force. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_force_per_unit_length(self) -> '_1438.ForcePerUnitLength':
        """ForcePerUnitLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1438.ForcePerUnitLength.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ForcePerUnitLength. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_force_per_unit_pressure(self) -> '_1439.ForcePerUnitPressure':
        """ForcePerUnitPressure: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1439.ForcePerUnitPressure.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ForcePerUnitPressure. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_force_per_unit_temperature(self) -> '_1440.ForcePerUnitTemperature':
        """ForcePerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1440.ForcePerUnitTemperature.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ForcePerUnitTemperature. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_fraction_measurement_base(self) -> '_1441.FractionMeasurementBase':
        """FractionMeasurementBase: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1441.FractionMeasurementBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FractionMeasurementBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_frequency(self) -> '_1442.Frequency':
        """Frequency: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1442.Frequency.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Frequency. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_fuel_consumption_engine(self) -> '_1443.FuelConsumptionEngine':
        """FuelConsumptionEngine: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1443.FuelConsumptionEngine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FuelConsumptionEngine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_fuel_efficiency_vehicle(self) -> '_1444.FuelEfficiencyVehicle':
        """FuelEfficiencyVehicle: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1444.FuelEfficiencyVehicle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FuelEfficiencyVehicle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_gradient(self) -> '_1445.Gradient':
        """Gradient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1445.Gradient.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Gradient. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_heat_conductivity(self) -> '_1446.HeatConductivity':
        """HeatConductivity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1446.HeatConductivity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatConductivity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_heat_transfer(self) -> '_1447.HeatTransfer':
        """HeatTransfer: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1447.HeatTransfer.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatTransfer. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self) -> '_1448.HeatTransferCoefficientForPlasticGearTooth':
        """HeatTransferCoefficientForPlasticGearTooth: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1448.HeatTransferCoefficientForPlasticGearTooth.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatTransferCoefficientForPlasticGearTooth. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_heat_transfer_resistance(self) -> '_1449.HeatTransferResistance':
        """HeatTransferResistance: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1449.HeatTransferResistance.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatTransferResistance. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_impulse(self) -> '_1450.Impulse':
        """Impulse: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1450.Impulse.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Impulse. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_index(self) -> '_1451.Index':
        """Index: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1451.Index.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Index. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_integer(self) -> '_1452.Integer':
        """Integer: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1452.Integer.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Integer. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_inverse_short_length(self) -> '_1453.InverseShortLength':
        """InverseShortLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1453.InverseShortLength.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to InverseShortLength. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_inverse_short_time(self) -> '_1454.InverseShortTime':
        """InverseShortTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1454.InverseShortTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to InverseShortTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_jerk(self) -> '_1455.Jerk':
        """Jerk: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1455.Jerk.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Jerk. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_kinematic_viscosity(self) -> '_1456.KinematicViscosity':
        """KinematicViscosity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1456.KinematicViscosity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to KinematicViscosity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_length_long(self) -> '_1457.LengthLong':
        """LengthLong: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1457.LengthLong.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthLong. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_length_medium(self) -> '_1458.LengthMedium':
        """LengthMedium: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1458.LengthMedium.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthMedium. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_length_per_unit_temperature(self) -> '_1459.LengthPerUnitTemperature':
        """LengthPerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1459.LengthPerUnitTemperature.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthPerUnitTemperature. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_length_short(self) -> '_1460.LengthShort':
        """LengthShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1460.LengthShort.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthShort. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_length_to_the_fourth(self) -> '_1461.LengthToTheFourth':
        """LengthToTheFourth: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1461.LengthToTheFourth.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthToTheFourth. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_length_very_long(self) -> '_1462.LengthVeryLong':
        """LengthVeryLong: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1462.LengthVeryLong.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthVeryLong. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_length_very_short(self) -> '_1463.LengthVeryShort':
        """LengthVeryShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1463.LengthVeryShort.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthVeryShort. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_length_very_short_per_length_short(self) -> '_1464.LengthVeryShortPerLengthShort':
        """LengthVeryShortPerLengthShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1464.LengthVeryShortPerLengthShort.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthVeryShortPerLengthShort. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_linear_angular_damping(self) -> '_1465.LinearAngularDamping':
        """LinearAngularDamping: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1465.LinearAngularDamping.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearAngularDamping. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_linear_angular_stiffness_cross_term(self) -> '_1466.LinearAngularStiffnessCrossTerm':
        """LinearAngularStiffnessCrossTerm: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1466.LinearAngularStiffnessCrossTerm.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearAngularStiffnessCrossTerm. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_linear_damping(self) -> '_1467.LinearDamping':
        """LinearDamping: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1467.LinearDamping.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearDamping. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_linear_flexibility(self) -> '_1468.LinearFlexibility':
        """LinearFlexibility: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1468.LinearFlexibility.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearFlexibility. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_linear_stiffness(self) -> '_1469.LinearStiffness':
        """LinearStiffness: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1469.LinearStiffness.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearStiffness. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_mass(self) -> '_1470.Mass':
        """Mass: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1470.Mass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Mass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_mass_per_unit_length(self) -> '_1471.MassPerUnitLength':
        """MassPerUnitLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1471.MassPerUnitLength.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MassPerUnitLength. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_mass_per_unit_time(self) -> '_1472.MassPerUnitTime':
        """MassPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1472.MassPerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MassPerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_moment_of_inertia(self) -> '_1473.MomentOfInertia':
        """MomentOfInertia: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1473.MomentOfInertia.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MomentOfInertia. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_moment_of_inertia_per_unit_length(self) -> '_1474.MomentOfInertiaPerUnitLength':
        """MomentOfInertiaPerUnitLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1474.MomentOfInertiaPerUnitLength.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MomentOfInertiaPerUnitLength. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_moment_per_unit_pressure(self) -> '_1475.MomentPerUnitPressure':
        """MomentPerUnitPressure: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1475.MomentPerUnitPressure.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MomentPerUnitPressure. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_number(self) -> '_1476.Number':
        """Number: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1476.Number.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Number. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_percentage(self) -> '_1477.Percentage':
        """Percentage: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1477.Percentage.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Percentage. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_power(self) -> '_1478.Power':
        """Power: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1478.Power.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Power. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_power_per_small_area(self) -> '_1479.PowerPerSmallArea':
        """PowerPerSmallArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1479.PowerPerSmallArea.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerPerSmallArea. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_power_per_unit_time(self) -> '_1480.PowerPerUnitTime':
        """PowerPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1480.PowerPerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerPerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_power_small(self) -> '_1481.PowerSmall':
        """PowerSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1481.PowerSmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_power_small_per_area(self) -> '_1482.PowerSmallPerArea':
        """PowerSmallPerArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1482.PowerSmallPerArea.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmallPerArea. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_power_small_per_unit_area_per_unit_time(self) -> '_1483.PowerSmallPerUnitAreaPerUnitTime':
        """PowerSmallPerUnitAreaPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1483.PowerSmallPerUnitAreaPerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmallPerUnitAreaPerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_power_small_per_unit_time(self) -> '_1484.PowerSmallPerUnitTime':
        """PowerSmallPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1484.PowerSmallPerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmallPerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_pressure(self) -> '_1485.Pressure':
        """Pressure: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1485.Pressure.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Pressure. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_pressure_per_unit_time(self) -> '_1486.PressurePerUnitTime':
        """PressurePerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1486.PressurePerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PressurePerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_pressure_velocity_product(self) -> '_1487.PressureVelocityProduct':
        """PressureVelocityProduct: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1487.PressureVelocityProduct.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PressureVelocityProduct. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_pressure_viscosity_coefficient(self) -> '_1488.PressureViscosityCoefficient':
        """PressureViscosityCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1488.PressureViscosityCoefficient.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PressureViscosityCoefficient. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_price(self) -> '_1489.Price':
        """Price: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1489.Price.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Price. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_quadratic_angular_damping(self) -> '_1490.QuadraticAngularDamping':
        """QuadraticAngularDamping: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1490.QuadraticAngularDamping.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to QuadraticAngularDamping. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_quadratic_drag(self) -> '_1491.QuadraticDrag':
        """QuadraticDrag: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1491.QuadraticDrag.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to QuadraticDrag. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_rescaled_measurement(self) -> '_1492.RescaledMeasurement':
        """RescaledMeasurement: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1492.RescaledMeasurement.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to RescaledMeasurement. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_rotatum(self) -> '_1493.Rotatum':
        """Rotatum: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1493.Rotatum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Rotatum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_safety_factor(self) -> '_1494.SafetyFactor':
        """SafetyFactor: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1494.SafetyFactor.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SafetyFactor. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_specific_acoustic_impedance(self) -> '_1495.SpecificAcousticImpedance':
        """SpecificAcousticImpedance: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1495.SpecificAcousticImpedance.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SpecificAcousticImpedance. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_specific_heat(self) -> '_1496.SpecificHeat':
        """SpecificHeat: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1496.SpecificHeat.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SpecificHeat. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_square_root_of_unit_force_per_unit_area(self) -> '_1497.SquareRootOfUnitForcePerUnitArea':
        """SquareRootOfUnitForcePerUnitArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1497.SquareRootOfUnitForcePerUnitArea.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SquareRootOfUnitForcePerUnitArea. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_stiffness_per_unit_face_width(self) -> '_1498.StiffnessPerUnitFaceWidth':
        """StiffnessPerUnitFaceWidth: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1498.StiffnessPerUnitFaceWidth.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to StiffnessPerUnitFaceWidth. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_stress(self) -> '_1499.Stress':
        """Stress: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1499.Stress.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Stress. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_temperature(self) -> '_1500.Temperature':
        """Temperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1500.Temperature.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Temperature. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_temperature_difference(self) -> '_1501.TemperatureDifference':
        """TemperatureDifference: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1501.TemperatureDifference.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TemperatureDifference. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_temperature_per_unit_time(self) -> '_1502.TemperaturePerUnitTime':
        """TemperaturePerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1502.TemperaturePerUnitTime.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TemperaturePerUnitTime. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_text(self) -> '_1503.Text':
        """Text: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1503.Text.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Text. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_thermal_contact_coefficient(self) -> '_1504.ThermalContactCoefficient':
        """ThermalContactCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1504.ThermalContactCoefficient.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ThermalContactCoefficient. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_thermal_expansion_coefficient(self) -> '_1505.ThermalExpansionCoefficient':
        """ThermalExpansionCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1505.ThermalExpansionCoefficient.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ThermalExpansionCoefficient. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_thermo_elastic_factor(self) -> '_1506.ThermoElasticFactor':
        """ThermoElasticFactor: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1506.ThermoElasticFactor.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ThermoElasticFactor. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_time(self) -> '_1507.Time':
        """Time: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1507.Time.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Time. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_time_short(self) -> '_1508.TimeShort':
        """TimeShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1508.TimeShort.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TimeShort. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_time_very_short(self) -> '_1509.TimeVeryShort':
        """TimeVeryShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1509.TimeVeryShort.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TimeVeryShort. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_torque(self) -> '_1510.Torque':
        """Torque: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1510.Torque.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Torque. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_torque_converter_inverse_k(self) -> '_1511.TorqueConverterInverseK':
        """TorqueConverterInverseK: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1511.TorqueConverterInverseK.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TorqueConverterInverseK. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_torque_converter_k(self) -> '_1512.TorqueConverterK':
        """TorqueConverterK: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1512.TorqueConverterK.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TorqueConverterK. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_torque_per_unit_temperature(self) -> '_1513.TorquePerUnitTemperature':
        """TorquePerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1513.TorquePerUnitTemperature.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TorquePerUnitTemperature. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_velocity(self) -> '_1514.Velocity':
        """Velocity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1514.Velocity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Velocity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_velocity_small(self) -> '_1515.VelocitySmall':
        """VelocitySmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1515.VelocitySmall.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to VelocitySmall. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_viscosity(self) -> '_1516.Viscosity':
        """Viscosity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1516.Viscosity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Viscosity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_voltage(self) -> '_1517.Voltage':
        """Voltage: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1517.Voltage.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Voltage. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_volume(self) -> '_1518.Volume':
        """Volume: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1518.Volume.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Volume. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_wear_coefficient(self) -> '_1519.WearCoefficient':
        """WearCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1519.WearCoefficient.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to WearCoefficient. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def current_selected_measurement_of_type_yank(self) -> '_1520.Yank':
        """Yank: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentSelectedMeasurement

        if temp is None:
            return None

        if _1520.Yank.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Yank. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def default_to_imperial(self):
        """ 'DefaultToImperial' is the original name of this method."""

        self.wrapped.DefaultToImperial()

    def default_to_metric(self):
        """ 'DefaultToMetric' is the original name of this method."""

        self.wrapped.DefaultToMetric()

    def find_measurement_by_name(self, name: 'str') -> '_1406.MeasurementBase':
        """ 'FindMeasurementByName' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.utility.units_and_measurements.MeasurementBase
        """

        name = str(name)
        method_result = self.wrapped.FindMeasurementByName(name if name else '')
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def get_measurement(self, measurement_type: '_7286.MeasurementType') -> '_1406.MeasurementBase':
        """ 'GetMeasurement' is the original name of this method.

        Args:
            measurement_type (mastapy.units_and_measurements.MeasurementType)

        Returns:
            mastapy.utility.units_and_measurements.MeasurementBase
        """

        measurement_type = conversion.mp_to_pn_enum(measurement_type)
        method_result = self.wrapped.GetMeasurement(measurement_type)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
