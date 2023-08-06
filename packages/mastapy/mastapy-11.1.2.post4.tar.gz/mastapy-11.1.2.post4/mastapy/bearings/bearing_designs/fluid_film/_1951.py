"""_1951.py

TiltingPadThrustBearing
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings import _1664
from mastapy.bearings.bearing_designs.fluid_film import _1943
from mastapy._internal.python_net import python_net_import

_TILTING_PAD_THRUST_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'TiltingPadThrustBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('TiltingPadThrustBearing',)


class TiltingPadThrustBearing(_1943.PadFluidFilmBearing):
    """TiltingPadThrustBearing

    This is a mastapy class.
    """

    TYPE = _TILTING_PAD_THRUST_BEARING

    def __init__(self, instance_to_wrap: 'TiltingPadThrustBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def non_dimensional_friction(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'NonDimensionalFriction' is the original name of this property."""

        temp = self.wrapped.NonDimensionalFriction

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @non_dimensional_friction.setter
    def non_dimensional_friction(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NonDimensionalFriction = value

    @property
    def non_dimensional_inlet_flow(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'NonDimensionalInletFlow' is the original name of this property."""

        temp = self.wrapped.NonDimensionalInletFlow

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @non_dimensional_inlet_flow.setter
    def non_dimensional_inlet_flow(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NonDimensionalInletFlow = value

    @property
    def non_dimensional_load(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'NonDimensionalLoad' is the original name of this property."""

        temp = self.wrapped.NonDimensionalLoad

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @non_dimensional_load.setter
    def non_dimensional_load(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NonDimensionalLoad = value

    @property
    def non_dimensional_minimum_film_thickness(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'NonDimensionalMinimumFilmThickness' is the original name of this property."""

        temp = self.wrapped.NonDimensionalMinimumFilmThickness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @non_dimensional_minimum_film_thickness.setter
    def non_dimensional_minimum_film_thickness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NonDimensionalMinimumFilmThickness = value

    @property
    def non_dimensional_side_flow(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'NonDimensionalSideFlow' is the original name of this property."""

        temp = self.wrapped.NonDimensionalSideFlow

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @non_dimensional_side_flow.setter
    def non_dimensional_side_flow(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NonDimensionalSideFlow = value

    @property
    def pad_circumferential_width(self) -> 'float':
        """float: 'PadCircumferentialWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PadCircumferentialWidth

        if temp is None:
            return None

        return temp

    @property
    def pad_height(self) -> 'float':
        """float: 'PadHeight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PadHeight

        if temp is None:
            return None

        return temp

    @property
    def pad_height_aspect_ratio(self) -> 'float':
        """float: 'PadHeightAspectRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PadHeightAspectRatio

        if temp is None:
            return None

        return temp

    @property
    def pad_inner_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PadInnerDiameter' is the original name of this property."""

        temp = self.wrapped.PadInnerDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @pad_inner_diameter.setter
    def pad_inner_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PadInnerDiameter = value

    @property
    def pad_outer_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PadOuterDiameter' is the original name of this property."""

        temp = self.wrapped.PadOuterDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @pad_outer_diameter.setter
    def pad_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PadOuterDiameter = value

    @property
    def pad_width_aspect_ratio(self) -> 'float':
        """float: 'PadWidthAspectRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PadWidthAspectRatio

        if temp is None:
            return None

        return temp

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
    def tilting_pad_type(self) -> '_1664.TiltingPadTypes':
        """TiltingPadTypes: 'TiltingPadType' is the original name of this property."""

        temp = self.wrapped.TiltingPadType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1664.TiltingPadTypes)(value) if value is not None else None

    @tilting_pad_type.setter
    def tilting_pad_type(self, value: '_1664.TiltingPadTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TiltingPadType = value

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
