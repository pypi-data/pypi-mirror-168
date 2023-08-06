"""_6663.py

PlanetManufactureError
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PLANET_MANUFACTURE_ERROR = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PlanetManufactureError')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetManufactureError',)


class PlanetManufactureError(_0.APIBase):
    """PlanetManufactureError

    This is a mastapy class.
    """

    TYPE = _PLANET_MANUFACTURE_ERROR

    def __init__(self, instance_to_wrap: 'PlanetManufactureError.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle_of_error_in_pin_coordinate_system(self) -> 'float':
        """float: 'AngleOfErrorInPinCoordinateSystem' is the original name of this property."""

        temp = self.wrapped.AngleOfErrorInPinCoordinateSystem

        if temp is None:
            return None

        return temp

    @angle_of_error_in_pin_coordinate_system.setter
    def angle_of_error_in_pin_coordinate_system(self, value: 'float'):
        self.wrapped.AngleOfErrorInPinCoordinateSystem = float(value) if value else 0.0

    @property
    def angular_error(self) -> 'float':
        """float: 'AngularError' is the original name of this property."""

        temp = self.wrapped.AngularError

        if temp is None:
            return None

        return temp

    @angular_error.setter
    def angular_error(self, value: 'float'):
        self.wrapped.AngularError = float(value) if value else 0.0

    @property
    def hole_radial_displacement(self) -> 'float':
        """float: 'HoleRadialDisplacement' is the original name of this property."""

        temp = self.wrapped.HoleRadialDisplacement

        if temp is None:
            return None

        return temp

    @hole_radial_displacement.setter
    def hole_radial_displacement(self, value: 'float'):
        self.wrapped.HoleRadialDisplacement = float(value) if value else 0.0

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def radial_error(self) -> 'float':
        """float: 'RadialError' is the original name of this property."""

        temp = self.wrapped.RadialError

        if temp is None:
            return None

        return temp

    @radial_error.setter
    def radial_error(self, value: 'float'):
        self.wrapped.RadialError = float(value) if value else 0.0

    @property
    def radial_error_carrier(self) -> 'float':
        """float: 'RadialErrorCarrier' is the original name of this property."""

        temp = self.wrapped.RadialErrorCarrier

        if temp is None:
            return None

        return temp

    @radial_error_carrier.setter
    def radial_error_carrier(self, value: 'float'):
        self.wrapped.RadialErrorCarrier = float(value) if value else 0.0

    @property
    def radial_tilt_error(self) -> 'float':
        """float: 'RadialTiltError' is the original name of this property."""

        temp = self.wrapped.RadialTiltError

        if temp is None:
            return None

        return temp

    @radial_tilt_error.setter
    def radial_tilt_error(self, value: 'float'):
        self.wrapped.RadialTiltError = float(value) if value else 0.0

    @property
    def tangential_error(self) -> 'float':
        """float: 'TangentialError' is the original name of this property."""

        temp = self.wrapped.TangentialError

        if temp is None:
            return None

        return temp

    @tangential_error.setter
    def tangential_error(self, value: 'float'):
        self.wrapped.TangentialError = float(value) if value else 0.0

    @property
    def tangential_tilt_error(self) -> 'float':
        """float: 'TangentialTiltError' is the original name of this property."""

        temp = self.wrapped.TangentialTiltError

        if temp is None:
            return None

        return temp

    @tangential_tilt_error.setter
    def tangential_tilt_error(self, value: 'float'):
        self.wrapped.TangentialTiltError = float(value) if value else 0.0

    @property
    def x_error(self) -> 'float':
        """float: 'XError' is the original name of this property."""

        temp = self.wrapped.XError

        if temp is None:
            return None

        return temp

    @x_error.setter
    def x_error(self, value: 'float'):
        self.wrapped.XError = float(value) if value else 0.0

    @property
    def x_tilt_error(self) -> 'float':
        """float: 'XTiltError' is the original name of this property."""

        temp = self.wrapped.XTiltError

        if temp is None:
            return None

        return temp

    @x_tilt_error.setter
    def x_tilt_error(self, value: 'float'):
        self.wrapped.XTiltError = float(value) if value else 0.0

    @property
    def y_error(self) -> 'float':
        """float: 'YError' is the original name of this property."""

        temp = self.wrapped.YError

        if temp is None:
            return None

        return temp

    @y_error.setter
    def y_error(self, value: 'float'):
        self.wrapped.YError = float(value) if value else 0.0

    @property
    def y_tilt_error(self) -> 'float':
        """float: 'YTiltError' is the original name of this property."""

        temp = self.wrapped.YTiltError

        if temp is None:
            return None

        return temp

    @y_tilt_error.setter
    def y_tilt_error(self, value: 'float'):
        self.wrapped.YTiltError = float(value) if value else 0.0
