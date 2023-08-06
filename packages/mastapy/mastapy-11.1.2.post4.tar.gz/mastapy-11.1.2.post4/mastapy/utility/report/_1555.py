"""_1555.py

CustomReportTabs
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.utility.report import _1544, _1554
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_TABS = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportTabs')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportTabs',)


class CustomReportTabs(_1544.CustomReportItemContainerCollection['_1554.CustomReportTab']):
    """CustomReportTabs

    This is a mastapy class.
    """

    TYPE = _CUSTOM_REPORT_TABS

    def __init__(self, instance_to_wrap: 'CustomReportTabs.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_main_report_item(self) -> 'bool':
        """bool: 'IsMainReportItem' is the original name of this property."""

        temp = self.wrapped.IsMainReportItem

        if temp is None:
            return None

        return temp

    @is_main_report_item.setter
    def is_main_report_item(self, value: 'bool'):
        self.wrapped.IsMainReportItem = bool(value) if value else False

    @property
    def number_of_tabs(self) -> 'int':
        """int: 'NumberOfTabs' is the original name of this property."""

        temp = self.wrapped.NumberOfTabs

        if temp is None:
            return None

        return temp

    @number_of_tabs.setter
    def number_of_tabs(self, value: 'int'):
        self.wrapped.NumberOfTabs = int(value) if value else 0

    @property
    def layout_orientation(self) -> 'CustomReportTabs.ReportLayoutOrientation':
        """ReportLayoutOrientation: 'LayoutOrientation' is the original name of this property."""

        temp = self.wrapped.LayoutOrientation

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(CustomReportTabs.ReportLayoutOrientation)(value) if value is not None else None

    @layout_orientation.setter
    def layout_orientation(self, value: 'CustomReportTabs.ReportLayoutOrientation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.LayoutOrientation = value

    @property
    def scroll_content(self) -> 'bool':
        """bool: 'ScrollContent' is the original name of this property."""

        temp = self.wrapped.ScrollContent

        if temp is None:
            return None

        return temp

    @scroll_content.setter
    def scroll_content(self, value: 'bool'):
        self.wrapped.ScrollContent = bool(value) if value else False
