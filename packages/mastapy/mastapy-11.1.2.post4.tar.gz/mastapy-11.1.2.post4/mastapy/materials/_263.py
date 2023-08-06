"""_263.py

VehicleDynamicsProperties
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_VEHICLE_DYNAMICS_PROPERTIES = python_net_import('SMT.MastaAPI.Materials', 'VehicleDynamicsProperties')


__docformat__ = 'restructuredtext en'
__all__ = ('VehicleDynamicsProperties',)


class VehicleDynamicsProperties(_0.APIBase):
    """VehicleDynamicsProperties

    This is a mastapy class.
    """

    TYPE = _VEHICLE_DYNAMICS_PROPERTIES

    def __init__(self, instance_to_wrap: 'VehicleDynamicsProperties.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def aerodynamic_drag_coefficient(self) -> 'float':
        """float: 'AerodynamicDragCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AerodynamicDragCoefficient

        if temp is None:
            return None

        return temp

    @property
    def air_density(self) -> 'float':
        """float: 'AirDensity' is the original name of this property."""

        temp = self.wrapped.AirDensity

        if temp is None:
            return None

        return temp

    @air_density.setter
    def air_density(self, value: 'float'):
        self.wrapped.AirDensity = float(value) if value else 0.0

    @property
    def drag_coefficient(self) -> 'float':
        """float: 'DragCoefficient' is the original name of this property."""

        temp = self.wrapped.DragCoefficient

        if temp is None:
            return None

        return temp

    @drag_coefficient.setter
    def drag_coefficient(self, value: 'float'):
        self.wrapped.DragCoefficient = float(value) if value else 0.0

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
    def rolling_radius(self) -> 'float':
        """float: 'RollingRadius' is the original name of this property."""

        temp = self.wrapped.RollingRadius

        if temp is None:
            return None

        return temp

    @rolling_radius.setter
    def rolling_radius(self, value: 'float'):
        self.wrapped.RollingRadius = float(value) if value else 0.0

    @property
    def rolling_resistance(self) -> 'float':
        """float: 'RollingResistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollingResistance

        if temp is None:
            return None

        return temp

    @property
    def rolling_resistance_coefficient(self) -> 'float':
        """float: 'RollingResistanceCoefficient' is the original name of this property."""

        temp = self.wrapped.RollingResistanceCoefficient

        if temp is None:
            return None

        return temp

    @rolling_resistance_coefficient.setter
    def rolling_resistance_coefficient(self, value: 'float'):
        self.wrapped.RollingResistanceCoefficient = float(value) if value else 0.0

    @property
    def vehicle_effective_inertia(self) -> 'float':
        """float: 'VehicleEffectiveInertia' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VehicleEffectiveInertia

        if temp is None:
            return None

        return temp

    @property
    def vehicle_effective_mass(self) -> 'float':
        """float: 'VehicleEffectiveMass' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VehicleEffectiveMass

        if temp is None:
            return None

        return temp

    @property
    def vehicle_frontal_area(self) -> 'float':
        """float: 'VehicleFrontalArea' is the original name of this property."""

        temp = self.wrapped.VehicleFrontalArea

        if temp is None:
            return None

        return temp

    @vehicle_frontal_area.setter
    def vehicle_frontal_area(self, value: 'float'):
        self.wrapped.VehicleFrontalArea = float(value) if value else 0.0

    @property
    def vehicle_mass(self) -> 'float':
        """float: 'VehicleMass' is the original name of this property."""

        temp = self.wrapped.VehicleMass

        if temp is None:
            return None

        return temp

    @vehicle_mass.setter
    def vehicle_mass(self, value: 'float'):
        self.wrapped.VehicleMass = float(value) if value else 0.0

    @property
    def wheel_inertia(self) -> 'float':
        """float: 'WheelInertia' is the original name of this property."""

        temp = self.wrapped.WheelInertia

        if temp is None:
            return None

        return temp

    @wheel_inertia.setter
    def wheel_inertia(self, value: 'float'):
        self.wrapped.WheelInertia = float(value) if value else 0.0
