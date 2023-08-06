"""_1890.py

DummyRollingBearing
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_designs import _1888
from mastapy._internal.python_net import python_net_import

_DUMMY_ROLLING_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns', 'DummyRollingBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('DummyRollingBearing',)


class DummyRollingBearing(_1888.BearingDesign):
    """DummyRollingBearing

    This is a mastapy class.
    """

    TYPE = _DUMMY_ROLLING_BEARING

    def __init__(self, instance_to_wrap: 'DummyRollingBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bore(self) -> 'float':
        """float: 'Bore' is the original name of this property."""

        temp = self.wrapped.Bore

        if temp is None:
            return None

        return temp

    @bore.setter
    def bore(self, value: 'float'):
        self.wrapped.Bore = float(value) if value else 0.0

    @property
    def outer_diameter(self) -> 'float':
        """float: 'OuterDiameter' is the original name of this property."""

        temp = self.wrapped.OuterDiameter

        if temp is None:
            return None

        return temp

    @outer_diameter.setter
    def outer_diameter(self, value: 'float'):
        self.wrapped.OuterDiameter = float(value) if value else 0.0

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
