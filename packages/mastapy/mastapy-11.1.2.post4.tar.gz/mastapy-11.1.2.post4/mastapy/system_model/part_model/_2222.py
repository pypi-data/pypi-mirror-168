"""_2222.py

PowerLoad
"""


from mastapy._internal.python_net import python_net_import
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.math_utility.measured_data import _1373
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.system_model import _1973
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.analyses_and_results.static_loads import _6594
from mastapy.materials.efficiency import _272
from mastapy.system_model.part_model import _2231, _2229

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoad',)


class PowerLoad(_2229.VirtualComponent):
    """PowerLoad

    This is a mastapy class.
    """

    TYPE = _POWER_LOAD

    def __init__(self, instance_to_wrap: 'PowerLoad.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def electric_machine_detail_database(self) -> 'str':
        """str: 'ElectricMachineDetailDatabase' is the original name of this property."""

        temp = self.wrapped.ElectricMachineDetailDatabase.SelectedItemName

        if temp is None:
            return None

        return temp

    @electric_machine_detail_database.setter
    def electric_machine_detail_database(self, value: 'str'):
        self.wrapped.ElectricMachineDetailDatabase.SetSelectedItem(str(value) if value else '')

    @property
    def engine_fuel_consumption_grid(self) -> '_1373.GriddedSurfaceAccessor':
        """GriddedSurfaceAccessor: 'EngineFuelConsumptionGrid' is the original name of this property."""

        temp = self.wrapped.EngineFuelConsumptionGrid

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @engine_fuel_consumption_grid.setter
    def engine_fuel_consumption_grid(self, value: '_1373.GriddedSurfaceAccessor'):
        value = value.wrapped if value else None
        self.wrapped.EngineFuelConsumptionGrid = value

    @property
    def engine_torque_grid(self) -> '_1373.GriddedSurfaceAccessor':
        """GriddedSurfaceAccessor: 'EngineTorqueGrid' is the original name of this property."""

        temp = self.wrapped.EngineTorqueGrid

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @engine_torque_grid.setter
    def engine_torque_grid(self, value: '_1373.GriddedSurfaceAccessor'):
        value = value.wrapped if value else None
        self.wrapped.EngineTorqueGrid = value

    @property
    def number_of_wheels(self) -> 'int':
        """int: 'NumberOfWheels' is the original name of this property."""

        temp = self.wrapped.NumberOfWheels

        if temp is None:
            return None

        return temp

    @number_of_wheels.setter
    def number_of_wheels(self, value: 'int'):
        self.wrapped.NumberOfWheels = int(value) if value else 0

    @property
    def number_of_blades(self) -> 'int':
        """int: 'NumberOfBlades' is the original name of this property."""

        temp = self.wrapped.NumberOfBlades

        if temp is None:
            return None

        return temp

    @number_of_blades.setter
    def number_of_blades(self, value: 'int'):
        self.wrapped.NumberOfBlades = int(value) if value else 0

    @property
    def positive_is_forwards(self) -> 'bool':
        """bool: 'PositiveIsForwards' is the original name of this property."""

        temp = self.wrapped.PositiveIsForwards

        if temp is None:
            return None

        return temp

    @positive_is_forwards.setter
    def positive_is_forwards(self, value: 'bool'):
        self.wrapped.PositiveIsForwards = bool(value) if value else False

    @property
    def power_load_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_PowerLoadType':
        """enum_with_selected_value.EnumWithSelectedValue_PowerLoadType: 'PowerLoadType' is the original name of this property."""

        temp = self.wrapped.PowerLoadType

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_PowerLoadType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @power_load_type.setter
    def power_load_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_PowerLoadType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PowerLoadType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.PowerLoadType = value

    @property
    def torsional_stiffness(self) -> 'float':
        """float: 'TorsionalStiffness' is the original name of this property."""

        temp = self.wrapped.TorsionalStiffness

        if temp is None:
            return None

        return temp

    @torsional_stiffness.setter
    def torsional_stiffness(self, value: 'float'):
        self.wrapped.TorsionalStiffness = float(value) if value else 0.0

    @property
    def tyre_rolling_radius(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TyreRollingRadius' is the original name of this property."""

        temp = self.wrapped.TyreRollingRadius

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tyre_rolling_radius.setter
    def tyre_rolling_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.TyreRollingRadius = value

    @property
    def width_for_drawing(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'WidthForDrawing' is the original name of this property."""

        temp = self.wrapped.WidthForDrawing

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @width_for_drawing.setter
    def width_for_drawing(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.WidthForDrawing = value

    @property
    def electric_machine_detail(self) -> '_6594.ElectricMachineDetail':
        """ElectricMachineDetail: 'ElectricMachineDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElectricMachineDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def oil_pump_detail(self) -> '_272.OilPumpDetail':
        """OilPumpDetail: 'OilPumpDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OilPumpDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def single_blade_details(self) -> '_2231.WindTurbineSingleBladeDetails':
        """WindTurbineSingleBladeDetails: 'SingleBladeDetails' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SingleBladeDetails

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
