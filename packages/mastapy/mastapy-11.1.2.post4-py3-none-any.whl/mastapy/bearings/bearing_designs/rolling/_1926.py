"""_1926.py

SphericalRollerThrustBearing
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_designs.rolling import _1900
from mastapy._internal.python_net import python_net_import

_SPHERICAL_ROLLER_THRUST_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'SphericalRollerThrustBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('SphericalRollerThrustBearing',)


class SphericalRollerThrustBearing(_1900.BarrelRollerBearing):
    """SphericalRollerThrustBearing

    This is a mastapy class.
    """

    TYPE = _SPHERICAL_ROLLER_THRUST_BEARING

    def __init__(self, instance_to_wrap: 'SphericalRollerThrustBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle_between_roller_end_and_bearing_axis(self) -> 'float':
        """float: 'AngleBetweenRollerEndAndBearingAxis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngleBetweenRollerEndAndBearingAxis

        if temp is None:
            return None

        return temp

    @property
    def distance_to_pressure_point_from_left_face(self) -> 'float':
        """float: 'DistanceToPressurePointFromLeftFace' is the original name of this property."""

        temp = self.wrapped.DistanceToPressurePointFromLeftFace

        if temp is None:
            return None

        return temp

    @distance_to_pressure_point_from_left_face.setter
    def distance_to_pressure_point_from_left_face(self, value: 'float'):
        self.wrapped.DistanceToPressurePointFromLeftFace = float(value) if value else 0.0

    @property
    def element_centre_point_diameter(self) -> 'float':
        """float: 'ElementCentrePointDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElementCentrePointDiameter

        if temp is None:
            return None

        return temp

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
