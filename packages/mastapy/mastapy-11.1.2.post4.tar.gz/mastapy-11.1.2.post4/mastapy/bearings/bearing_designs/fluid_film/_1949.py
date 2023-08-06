"""_1949.py

PlainOilFedJournalBearing
"""


from mastapy.bearings import _1652
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.bearing_designs.fluid_film import (
    _1938, _1939, _1940, _1947
)
from mastapy._internal.python_net import python_net_import

_PLAIN_OIL_FED_JOURNAL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'PlainOilFedJournalBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('PlainOilFedJournalBearing',)


class PlainOilFedJournalBearing(_1947.PlainJournalBearing):
    """PlainOilFedJournalBearing

    This is a mastapy class.
    """

    TYPE = _PLAIN_OIL_FED_JOURNAL_BEARING

    def __init__(self, instance_to_wrap: 'PlainOilFedJournalBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def feed_type(self) -> '_1652.JournalOilFeedType':
        """JournalOilFeedType: 'FeedType' is the original name of this property."""

        temp = self.wrapped.FeedType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1652.JournalOilFeedType)(value) if value is not None else None

    @feed_type.setter
    def feed_type(self, value: '_1652.JournalOilFeedType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FeedType = value

    @property
    def land_width(self) -> 'float':
        """float: 'LandWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LandWidth

        if temp is None:
            return None

        return temp

    @property
    def number_of_axial_points_for_pressure_distribution(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfAxialPointsForPressureDistribution' is the original name of this property."""

        temp = self.wrapped.NumberOfAxialPointsForPressureDistribution

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_axial_points_for_pressure_distribution.setter
    def number_of_axial_points_for_pressure_distribution(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfAxialPointsForPressureDistribution = value

    @property
    def number_of_circumferential_points_for_pressure_distribution(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfCircumferentialPointsForPressureDistribution' is the original name of this property."""

        temp = self.wrapped.NumberOfCircumferentialPointsForPressureDistribution

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_circumferential_points_for_pressure_distribution.setter
    def number_of_circumferential_points_for_pressure_distribution(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfCircumferentialPointsForPressureDistribution = value

    @property
    def axial_groove_oil_feed(self) -> '_1938.AxialGrooveJournalBearing':
        """AxialGrooveJournalBearing: 'AxialGrooveOilFeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialGrooveOilFeed

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def axial_hole_oil_feed(self) -> '_1939.AxialHoleJournalBearing':
        """AxialHoleJournalBearing: 'AxialHoleOilFeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialHoleOilFeed

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def circumferential_groove_oil_feed(self) -> '_1940.CircumferentialFeedJournalBearing':
        """CircumferentialFeedJournalBearing: 'CircumferentialGrooveOilFeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CircumferentialGrooveOilFeed

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
