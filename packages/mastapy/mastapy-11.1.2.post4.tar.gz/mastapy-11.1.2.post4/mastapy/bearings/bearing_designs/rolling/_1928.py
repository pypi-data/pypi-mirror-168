"""_1928.py

ThreePointContactBallBearing
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.bearings.bearing_designs.rolling import _1915
from mastapy._internal.python_net import python_net_import

_THREE_POINT_CONTACT_BALL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'ThreePointContactBallBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('ThreePointContactBallBearing',)


class ThreePointContactBallBearing(_1915.MultiPointContactBallBearing):
    """ThreePointContactBallBearing

    This is a mastapy class.
    """

    TYPE = _THREE_POINT_CONTACT_BALL_BEARING

    def __init__(self, instance_to_wrap: 'ThreePointContactBallBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_radial_internal_clearance(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'AssemblyRadialInternalClearance' is the original name of this property."""

        temp = self.wrapped.AssemblyRadialInternalClearance

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @assembly_radial_internal_clearance.setter
    def assembly_radial_internal_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.AssemblyRadialInternalClearance = value

    @property
    def inner_shim_angle(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'InnerShimAngle' is the original name of this property."""

        temp = self.wrapped.InnerShimAngle

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @inner_shim_angle.setter
    def inner_shim_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.InnerShimAngle = value

    @property
    def inner_shim_width(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'InnerShimWidth' is the original name of this property."""

        temp = self.wrapped.InnerShimWidth

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @inner_shim_width.setter
    def inner_shim_width(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.InnerShimWidth = value
