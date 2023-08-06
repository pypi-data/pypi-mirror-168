"""_1950.py

TiltingPadJournalBearing
"""


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.bearing_designs.fluid_film import _1943
from mastapy._internal.python_net import python_net_import

_TILTING_PAD_JOURNAL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'TiltingPadJournalBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('TiltingPadJournalBearing',)


class TiltingPadJournalBearing(_1943.PadFluidFilmBearing):
    """TiltingPadJournalBearing

    This is a mastapy class.
    """

    TYPE = _TILTING_PAD_JOURNAL_BEARING

    def __init__(self, instance_to_wrap: 'TiltingPadJournalBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bearing_aspect_ratio(self) -> 'float':
        """float: 'BearingAspectRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingAspectRatio

        if temp is None:
            return None

        return temp

    @property
    def difference_between_pad_contact_surface_radius_and_bearing_inner_radius(self) -> 'float':
        """float: 'DifferenceBetweenPadContactSurfaceRadiusAndBearingInnerRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DifferenceBetweenPadContactSurfaceRadiusAndBearingInnerRadius

        if temp is None:
            return None

        return temp

    @property
    def pad_contact_surface_radius(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PadContactSurfaceRadius' is the original name of this property."""

        temp = self.wrapped.PadContactSurfaceRadius

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @pad_contact_surface_radius.setter
    def pad_contact_surface_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PadContactSurfaceRadius = value

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
