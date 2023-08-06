"""_617.py

PlungeShaverOutputs
"""


from typing import List

from PIL.Image import Image

from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _609, _615
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.gears.manufacturing.cylindrical import _593
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVER_OUTPUTS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'PlungeShaverOutputs')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShaverOutputs',)


class PlungeShaverOutputs(_0.APIBase):
    """PlungeShaverOutputs

    This is a mastapy class.
    """

    TYPE = _PLUNGE_SHAVER_OUTPUTS

    def __init__(self, instance_to_wrap: 'PlungeShaverOutputs.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def chart(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ChartType':
        """enum_with_selected_value.EnumWithSelectedValue_ChartType: 'Chart' is the original name of this property."""

        temp = self.wrapped.Chart

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ChartType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @chart.setter
    def chart(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ChartType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ChartType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.Chart = value

    @property
    def difference_between_chart_z_plane(self) -> 'float':
        """float: 'DifferenceBetweenChartZPlane' is the original name of this property."""

        temp = self.wrapped.DifferenceBetweenChartZPlane

        if temp is None:
            return None

        return temp

    @difference_between_chart_z_plane.setter
    def difference_between_chart_z_plane(self, value: 'float'):
        self.wrapped.DifferenceBetweenChartZPlane = float(value) if value else 0.0

    @property
    def profile_modification_on_conjugate_shaver_chart_left_flank(self) -> 'Image':
        """Image: 'ProfileModificationOnConjugateShaverChartLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileModificationOnConjugateShaverChartLeftFlank

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def profile_modification_on_conjugate_shaver_chart_right_flank(self) -> 'Image':
        """Image: 'ProfileModificationOnConjugateShaverChartRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileModificationOnConjugateShaverChartRightFlank

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def selected_flank(self) -> 'enum_with_selected_value.EnumWithSelectedValue_Flank':
        """enum_with_selected_value.EnumWithSelectedValue_Flank: 'SelectedFlank' is the original name of this property."""

        temp = self.wrapped.SelectedFlank

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_Flank.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @selected_flank.setter
    def selected_flank(self, value: 'enum_with_selected_value.EnumWithSelectedValue_Flank.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_Flank.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.SelectedFlank = value

    @property
    def shaved_gear_profile_modification_z_plane(self) -> 'float':
        """float: 'ShavedGearProfileModificationZPlane' is the original name of this property."""

        temp = self.wrapped.ShavedGearProfileModificationZPlane

        if temp is None:
            return None

        return temp

    @shaved_gear_profile_modification_z_plane.setter
    def shaved_gear_profile_modification_z_plane(self, value: 'float'):
        self.wrapped.ShavedGearProfileModificationZPlane = float(value) if value else 0.0

    @property
    def shaver_profile_modification_z_plane(self) -> 'float':
        """float: 'ShaverProfileModificationZPlane' is the original name of this property."""

        temp = self.wrapped.ShaverProfileModificationZPlane

        if temp is None:
            return None

        return temp

    @shaver_profile_modification_z_plane.setter
    def shaver_profile_modification_z_plane(self, value: 'float'):
        self.wrapped.ShaverProfileModificationZPlane = float(value) if value else 0.0

    @property
    def calculation_details(self) -> '_615.PlungeShaverGeneration':
        """PlungeShaverGeneration: 'CalculationDetails' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CalculationDetails

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

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
