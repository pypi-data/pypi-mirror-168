"""_5400.py

LoadCaseGroupHistograms
"""


from typing import List

from mastapy.utility_gui.charts import (
    _1634, _1625, _1630, _1631
)
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.cast_exception import CastException
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model import _2222
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_LOAD_CASE_GROUP_HISTOGRAMS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'LoadCaseGroupHistograms')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadCaseGroupHistograms',)


class LoadCaseGroupHistograms(_0.APIBase):
    """LoadCaseGroupHistograms

    This is a mastapy class.
    """

    TYPE = _LOAD_CASE_GROUP_HISTOGRAMS

    def __init__(self, instance_to_wrap: 'LoadCaseGroupHistograms.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def boost_pressure_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'BoostPressureChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoostPressureChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast boost_pressure_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def number_of_bins(self) -> 'int':
        """int: 'NumberOfBins' is the original name of this property."""

        temp = self.wrapped.NumberOfBins

        if temp is None:
            return None

        return temp

    @number_of_bins.setter
    def number_of_bins(self, value: 'int'):
        self.wrapped.NumberOfBins = int(value) if value else 0

    @property
    def power_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'PowerChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_load(self) -> 'list_with_selected_item.ListWithSelectedItem_PowerLoad':
        """list_with_selected_item.ListWithSelectedItem_PowerLoad: 'PowerLoad' is the original name of this property."""

        temp = self.wrapped.PowerLoad

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_PowerLoad)(temp) if temp is not None else None

    @power_load.setter
    def power_load(self, value: 'list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.PowerLoad = value

    @property
    def speed_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'SpeedChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpeedChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast speed_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def torque_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'TorqueChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast torque_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def y_axis_variable(self) -> 'LoadCaseGroupHistograms.RevolutionsOrDuration':
        """RevolutionsOrDuration: 'YAxisVariable' is the original name of this property."""

        temp = self.wrapped.YAxisVariable

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(LoadCaseGroupHistograms.RevolutionsOrDuration)(value) if value is not None else None

    @y_axis_variable.setter
    def y_axis_variable(self, value: 'LoadCaseGroupHistograms.RevolutionsOrDuration'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.YAxisVariable = value

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

    def run_power_flow(self):
        """ 'RunPowerFlow' is the original name of this method."""

        self.wrapped.RunPowerFlow()

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
