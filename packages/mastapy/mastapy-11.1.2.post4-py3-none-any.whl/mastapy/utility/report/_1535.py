"""_1535.py

CustomReportChart
"""


from mastapy._internal import constructor
from mastapy.utility.report import _1548, _1536
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_CHART = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportChart')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportChart',)


class CustomReportChart(_1548.CustomReportMultiPropertyItem['_1536.CustomReportChartItem']):
    """CustomReportChart

    This is a mastapy class.
    """

    TYPE = _CUSTOM_REPORT_CHART

    def __init__(self, instance_to_wrap: 'CustomReportChart.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def height(self) -> 'int':
        """int: 'Height' is the original name of this property."""

        temp = self.wrapped.Height

        if temp is None:
            return None

        return temp

    @height.setter
    def height(self, value: 'int'):
        self.wrapped.Height = int(value) if value else 0

    @property
    def width(self) -> 'int':
        """int: 'Width' is the original name of this property."""

        temp = self.wrapped.Width

        if temp is None:
            return None

        return temp

    @width.setter
    def width(self, value: 'int'):
        self.wrapped.Width = int(value) if value else 0
