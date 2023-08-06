"""_1943.py

PadFluidFilmBearing
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings import _1662
from mastapy.bearings.bearing_designs import _1889
from mastapy._internal.python_net import python_net_import

_PAD_FLUID_FILM_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'PadFluidFilmBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('PadFluidFilmBearing',)


class PadFluidFilmBearing(_1889.DetailedBearing):
    """PadFluidFilmBearing

    This is a mastapy class.
    """

    TYPE = _PAD_FLUID_FILM_BEARING

    def __init__(self, instance_to_wrap: 'PadFluidFilmBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def collar_surface_roughness(self) -> 'float':
        """float: 'CollarSurfaceRoughness' is the original name of this property."""

        temp = self.wrapped.CollarSurfaceRoughness

        if temp is None:
            return None

        return temp

    @collar_surface_roughness.setter
    def collar_surface_roughness(self, value: 'float'):
        self.wrapped.CollarSurfaceRoughness = float(value) if value else 0.0

    @property
    def limiting_film_thickness(self) -> 'float':
        """float: 'LimitingFilmThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LimitingFilmThickness

        if temp is None:
            return None

        return temp

    @property
    def number_of_pads(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfPads' is the original name of this property."""

        temp = self.wrapped.NumberOfPads

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_pads.setter
    def number_of_pads(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfPads = value

    @property
    def pad_angular_extent(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PadAngularExtent' is the original name of this property."""

        temp = self.wrapped.PadAngularExtent

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @pad_angular_extent.setter
    def pad_angular_extent(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PadAngularExtent = value

    @property
    def pivot_angular_offset(self) -> 'float':
        """float: 'PivotAngularOffset' is the original name of this property."""

        temp = self.wrapped.PivotAngularOffset

        if temp is None:
            return None

        return temp

    @pivot_angular_offset.setter
    def pivot_angular_offset(self, value: 'float'):
        self.wrapped.PivotAngularOffset = float(value) if value else 0.0

    @property
    def rotational_direction(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RotationalDirections':
        """enum_with_selected_value.EnumWithSelectedValue_RotationalDirections: 'RotationalDirection' is the original name of this property."""

        temp = self.wrapped.RotationalDirection

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RotationalDirections.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @rotational_direction.setter
    def rotational_direction(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RotationalDirections.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RotationalDirections.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.RotationalDirection = value
