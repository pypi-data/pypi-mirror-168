"""_1929.py

ThrustBallBearing
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings import _1654
from mastapy.bearings.bearing_designs.rolling import _1898
from mastapy._internal.python_net import python_net_import

_THRUST_BALL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'ThrustBallBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('ThrustBallBearing',)


class ThrustBallBearing(_1898.BallBearing):
    """ThrustBallBearing

    This is a mastapy class.
    """

    TYPE = _THRUST_BALL_BEARING

    def __init__(self, instance_to_wrap: 'ThrustBallBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def center_ring_corner_radius(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'CenterRingCornerRadius' is the original name of this property."""

        temp = self.wrapped.CenterRingCornerRadius

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @center_ring_corner_radius.setter
    def center_ring_corner_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.CenterRingCornerRadius = value

    @property
    def inner_ring_outer_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'InnerRingOuterDiameter' is the original name of this property."""

        temp = self.wrapped.InnerRingOuterDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @inner_ring_outer_diameter.setter
    def inner_ring_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.InnerRingOuterDiameter = value

    @property
    def outer_ring_inner_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OuterRingInnerDiameter' is the original name of this property."""

        temp = self.wrapped.OuterRingInnerDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @outer_ring_inner_diameter.setter
    def outer_ring_inner_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.OuterRingInnerDiameter = value

    @property
    def outer_ring_mounting(self) -> '_1654.OuterRingMounting':
        """OuterRingMounting: 'OuterRingMounting' is the original name of this property."""

        temp = self.wrapped.OuterRingMounting

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1654.OuterRingMounting)(value) if value is not None else None

    @outer_ring_mounting.setter
    def outer_ring_mounting(self, value: '_1654.OuterRingMounting'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OuterRingMounting = value

    @property
    def sphered_seat_offset(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SpheredSeatOffset' is the original name of this property."""

        temp = self.wrapped.SpheredSeatOffset

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @sphered_seat_offset.setter
    def sphered_seat_offset(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SpheredSeatOffset = value

    @property
    def sphered_seat_radius(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SpheredSeatRadius' is the original name of this property."""

        temp = self.wrapped.SpheredSeatRadius

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @sphered_seat_radius.setter
    def sphered_seat_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SpheredSeatRadius = value

    @property
    def sum_of_the_centre_and_inner_ring_left_corner_radius(self) -> 'float':
        """float: 'SumOfTheCentreAndInnerRingLeftCornerRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumOfTheCentreAndInnerRingLeftCornerRadius

        if temp is None:
            return None

        return temp

    @property
    def sum_of_the_centre_and_inner_ring_right_corner_radius(self) -> 'float':
        """float: 'SumOfTheCentreAndInnerRingRightCornerRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumOfTheCentreAndInnerRingRightCornerRadius

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
