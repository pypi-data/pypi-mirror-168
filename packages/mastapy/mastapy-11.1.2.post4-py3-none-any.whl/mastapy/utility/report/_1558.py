"""_1558.py

CustomSubReport
"""


from mastapy._internal import constructor
from mastapy.utility.report import _1539
from mastapy._internal.python_net import python_net_import

_CUSTOM_SUB_REPORT = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomSubReport')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomSubReport',)


class CustomSubReport(_1539.CustomReportDefinitionItem):
    """CustomSubReport

    This is a mastapy class.
    """

    TYPE = _CUSTOM_SUB_REPORT

    def __init__(self, instance_to_wrap: 'CustomSubReport.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def create_new_page(self) -> 'bool':
        """bool: 'CreateNewPage' is the original name of this property."""

        temp = self.wrapped.CreateNewPage

        if temp is None:
            return None

        return temp

    @create_new_page.setter
    def create_new_page(self, value: 'bool'):
        self.wrapped.CreateNewPage = bool(value) if value else False

    @property
    def scale(self) -> 'float':
        """float: 'Scale' is the original name of this property."""

        temp = self.wrapped.Scale

        if temp is None:
            return None

        return temp

    @scale.setter
    def scale(self, value: 'float'):
        self.wrapped.Scale = float(value) if value else 0.0

    @property
    def show_report_edit_toolbar(self) -> 'bool':
        """bool: 'ShowReportEditToolbar' is the original name of this property."""

        temp = self.wrapped.ShowReportEditToolbar

        if temp is None:
            return None

        return temp

    @show_report_edit_toolbar.setter
    def show_report_edit_toolbar(self, value: 'bool'):
        self.wrapped.ShowReportEditToolbar = bool(value) if value else False

    @property
    def show_table_of_contents(self) -> 'bool':
        """bool: 'ShowTableOfContents' is the original name of this property."""

        temp = self.wrapped.ShowTableOfContents

        if temp is None:
            return None

        return temp

    @show_table_of_contents.setter
    def show_table_of_contents(self, value: 'bool'):
        self.wrapped.ShowTableOfContents = bool(value) if value else False

    @property
    def show_as_report_in_the_editor(self) -> 'bool':
        """bool: 'ShowAsReportInTheEditor' is the original name of this property."""

        temp = self.wrapped.ShowAsReportInTheEditor

        if temp is None:
            return None

        return temp

    @show_as_report_in_the_editor.setter
    def show_as_report_in_the_editor(self, value: 'bool'):
        self.wrapped.ShowAsReportInTheEditor = bool(value) if value else False

    def report_source(self):
        """ 'ReportSource' is the original name of this method."""

        self.wrapped.ReportSource()
