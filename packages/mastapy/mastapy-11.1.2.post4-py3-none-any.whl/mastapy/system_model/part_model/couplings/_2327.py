"""_2327.py

Clutch
"""


from mastapy.math_utility.measured_data import _1373
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.part_model.couplings import _2329, _2332
from mastapy.math_utility import _1341
from mastapy.system_model.analyses_and_results.mbd_analyses import _5137
from mastapy.system_model.connections_and_sockets.couplings import _2093
from mastapy._internal.python_net import python_net_import

_CLUTCH = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Clutch')


__docformat__ = 'restructuredtext en'
__all__ = ('Clutch',)


class Clutch(_2332.Coupling):
    """Clutch

    This is a mastapy class.
    """

    TYPE = _CLUTCH

    def __init__(self, instance_to_wrap: 'Clutch.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angular_speed_temperature_grid(self) -> '_1373.GriddedSurfaceAccessor':
        """GriddedSurfaceAccessor: 'AngularSpeedTemperatureGrid' is the original name of this property."""

        temp = self.wrapped.AngularSpeedTemperatureGrid

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @angular_speed_temperature_grid.setter
    def angular_speed_temperature_grid(self, value: '_1373.GriddedSurfaceAccessor'):
        value = value.wrapped if value else None
        self.wrapped.AngularSpeedTemperatureGrid = value

    @property
    def area_of_friction_surface(self) -> 'float':
        """float: 'AreaOfFrictionSurface' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AreaOfFrictionSurface

        if temp is None:
            return None

        return temp

    @property
    def bore(self) -> 'float':
        """float: 'Bore' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bore

        if temp is None:
            return None

        return temp

    @property
    def clearance_between_friction_surfaces(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ClearanceBetweenFrictionSurfaces' is the original name of this property."""

        temp = self.wrapped.ClearanceBetweenFrictionSurfaces

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @clearance_between_friction_surfaces.setter
    def clearance_between_friction_surfaces(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ClearanceBetweenFrictionSurfaces = value

    @property
    def clutch_plate_temperature(self) -> 'float':
        """float: 'ClutchPlateTemperature' is the original name of this property."""

        temp = self.wrapped.ClutchPlateTemperature

        if temp is None:
            return None

        return temp

    @clutch_plate_temperature.setter
    def clutch_plate_temperature(self, value: 'float'):
        self.wrapped.ClutchPlateTemperature = float(value) if value else 0.0

    @property
    def clutch_specific_heat_capacity(self) -> 'float':
        """float: 'ClutchSpecificHeatCapacity' is the original name of this property."""

        temp = self.wrapped.ClutchSpecificHeatCapacity

        if temp is None:
            return None

        return temp

    @clutch_specific_heat_capacity.setter
    def clutch_specific_heat_capacity(self, value: 'float'):
        self.wrapped.ClutchSpecificHeatCapacity = float(value) if value else 0.0

    @property
    def clutch_thermal_mass(self) -> 'float':
        """float: 'ClutchThermalMass' is the original name of this property."""

        temp = self.wrapped.ClutchThermalMass

        if temp is None:
            return None

        return temp

    @clutch_thermal_mass.setter
    def clutch_thermal_mass(self, value: 'float'):
        self.wrapped.ClutchThermalMass = float(value) if value else 0.0

    @property
    def clutch_type(self) -> '_2329.ClutchType':
        """ClutchType: 'ClutchType' is the original name of this property."""

        temp = self.wrapped.ClutchType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2329.ClutchType)(value) if value is not None else None

    @clutch_type.setter
    def clutch_type(self, value: '_2329.ClutchType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ClutchType = value

    @property
    def clutch_to_oil_heat_transfer_coefficient(self) -> 'float':
        """float: 'ClutchToOilHeatTransferCoefficient' is the original name of this property."""

        temp = self.wrapped.ClutchToOilHeatTransferCoefficient

        if temp is None:
            return None

        return temp

    @clutch_to_oil_heat_transfer_coefficient.setter
    def clutch_to_oil_heat_transfer_coefficient(self, value: 'float'):
        self.wrapped.ClutchToOilHeatTransferCoefficient = float(value) if value else 0.0

    @property
    def diameter(self) -> 'float':
        """float: 'Diameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Diameter

        if temp is None:
            return None

        return temp

    @property
    def dynamic_coefficient_of_friction(self) -> 'float':
        """float: 'DynamicCoefficientOfFriction' is the original name of this property."""

        temp = self.wrapped.DynamicCoefficientOfFriction

        if temp is None:
            return None

        return temp

    @dynamic_coefficient_of_friction.setter
    def dynamic_coefficient_of_friction(self, value: 'float'):
        self.wrapped.DynamicCoefficientOfFriction = float(value) if value else 0.0

    @property
    def flow_rate_vs_speed(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'FlowRateVsSpeed' is the original name of this property."""

        temp = self.wrapped.FlowRateVsSpeed

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @flow_rate_vs_speed.setter
    def flow_rate_vs_speed(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.FlowRateVsSpeed = value

    @property
    def inner_diameter_of_friction_surface(self) -> 'float':
        """float: 'InnerDiameterOfFrictionSurface' is the original name of this property."""

        temp = self.wrapped.InnerDiameterOfFrictionSurface

        if temp is None:
            return None

        return temp

    @inner_diameter_of_friction_surface.setter
    def inner_diameter_of_friction_surface(self, value: 'float'):
        self.wrapped.InnerDiameterOfFrictionSurface = float(value) if value else 0.0

    @property
    def kiss_point_clutch_pressure(self) -> 'float':
        """float: 'KissPointClutchPressure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KissPointClutchPressure

        if temp is None:
            return None

        return temp

    @property
    def kiss_point_piston_pressure(self) -> 'float':
        """float: 'KissPointPistonPressure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KissPointPistonPressure

        if temp is None:
            return None

        return temp

    @property
    def kiss_point_pressure_percent(self) -> 'float':
        """float: 'KissPointPressurePercent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KissPointPressurePercent

        if temp is None:
            return None

        return temp

    @property
    def linear_speed_temperature_grid(self) -> '_1373.GriddedSurfaceAccessor':
        """GriddedSurfaceAccessor: 'LinearSpeedTemperatureGrid' is the original name of this property."""

        temp = self.wrapped.LinearSpeedTemperatureGrid

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @linear_speed_temperature_grid.setter
    def linear_speed_temperature_grid(self, value: '_1373.GriddedSurfaceAccessor'):
        value = value.wrapped if value else None
        self.wrapped.LinearSpeedTemperatureGrid = value

    @property
    def maximum_pressure_at_clutch(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MaximumPressureAtClutch' is the original name of this property."""

        temp = self.wrapped.MaximumPressureAtClutch

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @maximum_pressure_at_clutch.setter
    def maximum_pressure_at_clutch(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MaximumPressureAtClutch = value

    @property
    def maximum_pressure_at_piston(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MaximumPressureAtPiston' is the original name of this property."""

        temp = self.wrapped.MaximumPressureAtPiston

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @maximum_pressure_at_piston.setter
    def maximum_pressure_at_piston(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MaximumPressureAtPiston = value

    @property
    def number_of_friction_surfaces(self) -> 'int':
        """int: 'NumberOfFrictionSurfaces' is the original name of this property."""

        temp = self.wrapped.NumberOfFrictionSurfaces

        if temp is None:
            return None

        return temp

    @number_of_friction_surfaces.setter
    def number_of_friction_surfaces(self, value: 'int'):
        self.wrapped.NumberOfFrictionSurfaces = int(value) if value else 0

    @property
    def outer_diameter_of_friction_surface(self) -> 'float':
        """float: 'OuterDiameterOfFrictionSurface' is the original name of this property."""

        temp = self.wrapped.OuterDiameterOfFrictionSurface

        if temp is None:
            return None

        return temp

    @outer_diameter_of_friction_surface.setter
    def outer_diameter_of_friction_surface(self, value: 'float'):
        self.wrapped.OuterDiameterOfFrictionSurface = float(value) if value else 0.0

    @property
    def piston_area(self) -> 'float':
        """float: 'PistonArea' is the original name of this property."""

        temp = self.wrapped.PistonArea

        if temp is None:
            return None

        return temp

    @piston_area.setter
    def piston_area(self, value: 'float'):
        self.wrapped.PistonArea = float(value) if value else 0.0

    @property
    def specified_torque_capacity(self) -> 'float':
        """float: 'SpecifiedTorqueCapacity' is the original name of this property."""

        temp = self.wrapped.SpecifiedTorqueCapacity

        if temp is None:
            return None

        return temp

    @specified_torque_capacity.setter
    def specified_torque_capacity(self, value: 'float'):
        self.wrapped.SpecifiedTorqueCapacity = float(value) if value else 0.0

    @property
    def spring_preload(self) -> 'float':
        """float: 'SpringPreload' is the original name of this property."""

        temp = self.wrapped.SpringPreload

        if temp is None:
            return None

        return temp

    @spring_preload.setter
    def spring_preload(self, value: 'float'):
        self.wrapped.SpringPreload = float(value) if value else 0.0

    @property
    def spring_stiffness(self) -> 'float':
        """float: 'SpringStiffness' is the original name of this property."""

        temp = self.wrapped.SpringStiffness

        if temp is None:
            return None

        return temp

    @spring_stiffness.setter
    def spring_stiffness(self, value: 'float'):
        self.wrapped.SpringStiffness = float(value) if value else 0.0

    @property
    def spring_type(self) -> '_5137.ClutchSpringType':
        """ClutchSpringType: 'SpringType' is the original name of this property."""

        temp = self.wrapped.SpringType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5137.ClutchSpringType)(value) if value is not None else None

    @spring_type.setter
    def spring_type(self, value: '_5137.ClutchSpringType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SpringType = value

    @property
    def static_to_dynamic_friction_ratio(self) -> 'float':
        """float: 'StaticToDynamicFrictionRatio' is the original name of this property."""

        temp = self.wrapped.StaticToDynamicFrictionRatio

        if temp is None:
            return None

        return temp

    @static_to_dynamic_friction_ratio.setter
    def static_to_dynamic_friction_ratio(self, value: 'float'):
        self.wrapped.StaticToDynamicFrictionRatio = float(value) if value else 0.0

    @property
    def use_friction_coefficient_lookup(self) -> 'bool':
        """bool: 'UseFrictionCoefficientLookup' is the original name of this property."""

        temp = self.wrapped.UseFrictionCoefficientLookup

        if temp is None:
            return None

        return temp

    @use_friction_coefficient_lookup.setter
    def use_friction_coefficient_lookup(self, value: 'bool'):
        self.wrapped.UseFrictionCoefficientLookup = bool(value) if value else False

    @property
    def volumetric_oil_air_mixture_ratio(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'VolumetricOilAirMixtureRatio' is the original name of this property."""

        temp = self.wrapped.VolumetricOilAirMixtureRatio

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @volumetric_oil_air_mixture_ratio.setter
    def volumetric_oil_air_mixture_ratio(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.VolumetricOilAirMixtureRatio = value

    @property
    def width(self) -> 'float':
        """float: 'Width' is the original name of this property."""

        temp = self.wrapped.Width

        if temp is None:
            return None

        return temp

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value else 0.0

    @property
    def clutch_connection(self) -> '_2093.ClutchConnection':
        """ClutchConnection: 'ClutchConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClutchConnection

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
