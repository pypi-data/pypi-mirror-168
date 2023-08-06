"""_183.py

CoordinateSystemReporting
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.fe_tools.vis_tools_visualisation.enums import _1184
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_COORDINATE_SYSTEM_REPORTING = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'CoordinateSystemReporting')


__docformat__ = 'restructuredtext en'
__all__ = ('CoordinateSystemReporting',)


class CoordinateSystemReporting(_0.APIBase):
    """CoordinateSystemReporting

    This is a mastapy class.
    """

    TYPE = _COORDINATE_SYSTEM_REPORTING

    def __init__(self, instance_to_wrap: 'CoordinateSystemReporting.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def id(self) -> 'int':
        """int: 'ID' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ID

        if temp is None:
            return None

        return temp

    @property
    def origin(self) -> 'str':
        """str: 'Origin' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Origin

        if temp is None:
            return None

        return temp

    @property
    def type_(self) -> '_1184.CoordinateSystemType':
        """CoordinateSystemType: 'Type' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Type

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1184.CoordinateSystemType)(value) if value is not None else None

    @property
    def x_axis(self) -> 'str':
        """str: 'XAxis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.XAxis

        if temp is None:
            return None

        return temp

    @property
    def y_axis(self) -> 'str':
        """str: 'YAxis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YAxis

        if temp is None:
            return None

        return temp

    @property
    def z_axis(self) -> 'str':
        """str: 'ZAxis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZAxis

        if temp is None:
            return None

        return temp

    @property
    def report_names(self) -> 'List[str]':
        """List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    def output_default_report_to(self, file_path: 'str'):
        """ 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        """ 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        """ 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        """ 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        """ 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        """ 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        """

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
