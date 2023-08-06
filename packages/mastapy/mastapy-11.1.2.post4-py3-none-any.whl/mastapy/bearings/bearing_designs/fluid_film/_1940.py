"""_1940.py

CircumferentialFeedJournalBearing
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CIRCUMFERENTIAL_FEED_JOURNAL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'CircumferentialFeedJournalBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('CircumferentialFeedJournalBearing',)


class CircumferentialFeedJournalBearing(_0.APIBase):
    """CircumferentialFeedJournalBearing

    This is a mastapy class.
    """

    TYPE = _CIRCUMFERENTIAL_FEED_JOURNAL_BEARING

    def __init__(self, instance_to_wrap: 'CircumferentialFeedJournalBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def groove_width(self) -> 'float':
        """float: 'GrooveWidth' is the original name of this property."""

        temp = self.wrapped.GrooveWidth

        if temp is None:
            return None

        return temp

    @groove_width.setter
    def groove_width(self, value: 'float'):
        self.wrapped.GrooveWidth = float(value) if value else 0.0
