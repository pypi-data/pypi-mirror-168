"""_1550.py

CustomReportNameableItem
"""


from mastapy._internal import constructor
from mastapy.utility.report import _1542
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_NAMEABLE_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportNameableItem')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportNameableItem',)


class CustomReportNameableItem(_1542.CustomReportItem):
    """CustomReportNameableItem

    This is a mastapy class.
    """

    TYPE = _CUSTOM_REPORT_NAMEABLE_ITEM

    def __init__(self, instance_to_wrap: 'CustomReportNameableItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property."""

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else ''

    @property
    def x_position_for_cad(self) -> 'float':
        """float: 'XPositionForCAD' is the original name of this property."""

        temp = self.wrapped.XPositionForCAD

        if temp is None:
            return None

        return temp

    @x_position_for_cad.setter
    def x_position_for_cad(self, value: 'float'):
        self.wrapped.XPositionForCAD = float(value) if value else 0.0

    @property
    def y_position_for_cad(self) -> 'float':
        """float: 'YPositionForCAD' is the original name of this property."""

        temp = self.wrapped.YPositionForCAD

        if temp is None:
            return None

        return temp

    @y_position_for_cad.setter
    def y_position_for_cad(self, value: 'float'):
        self.wrapped.YPositionForCAD = float(value) if value else 0.0
