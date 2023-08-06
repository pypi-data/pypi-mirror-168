"""_1938.py

AxialGrooveJournalBearing
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_designs.fluid_film import _1937
from mastapy._internal.python_net import python_net_import

_AXIAL_GROOVE_JOURNAL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'AxialGrooveJournalBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('AxialGrooveJournalBearing',)


class AxialGrooveJournalBearing(_1937.AxialFeedJournalBearing):
    """AxialGrooveJournalBearing

    This is a mastapy class.
    """

    TYPE = _AXIAL_GROOVE_JOURNAL_BEARING

    def __init__(self, instance_to_wrap: 'AxialGrooveJournalBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def groove_length(self) -> 'float':
        """float: 'GrooveLength' is the original name of this property."""

        temp = self.wrapped.GrooveLength

        if temp is None:
            return None

        return temp

    @groove_length.setter
    def groove_length(self, value: 'float'):
        self.wrapped.GrooveLength = float(value) if value else 0.0

    @property
    def groove_radial_dimension(self) -> 'float':
        """float: 'GrooveRadialDimension' is the original name of this property."""

        temp = self.wrapped.GrooveRadialDimension

        if temp is None:
            return None

        return temp

    @groove_radial_dimension.setter
    def groove_radial_dimension(self, value: 'float'):
        self.wrapped.GrooveRadialDimension = float(value) if value else 0.0
