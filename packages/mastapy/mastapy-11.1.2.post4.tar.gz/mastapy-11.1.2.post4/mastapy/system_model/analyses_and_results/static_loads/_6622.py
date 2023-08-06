"""_6622.py

HarmonicLoadDataBase
"""


from typing import List

from mastapy._internal.implicit import enum_with_selected_value
from mastapy.system_model.analyses_and_results.static_loads import _6630
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.math_utility import _1320
from mastapy._internal.python_net import python_net_import
from mastapy.units_and_measurements import _7286
from mastapy import _0

_ARRAY = python_net_import('System', 'Array')
_DOUBLE = python_net_import('System', 'Double')
_STRING = python_net_import('System', 'String')
_MEASUREMENT_TYPE = python_net_import('SMT.MastaAPIUtility.UnitsAndMeasurements', 'MeasurementType')
_LIST = python_net_import('System.Collections.Generic', 'List')
_FOURIER_SERIES = python_net_import('SMT.MastaAPI.MathUtility', 'FourierSeries')
_HARMONIC_LOAD_DATA_BASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataBase')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataBase',)


class HarmonicLoadDataBase(_0.APIBase):
    """HarmonicLoadDataBase

    This is a mastapy class.
    """

    TYPE = _HARMONIC_LOAD_DATA_BASE

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def data_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType':
        """enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType: 'DataType' is the original name of this property."""

        temp = self.wrapped.DataType

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @data_type.setter
    def data_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DataType = value

    @property
    def excitation_order_as_rotational_order_of_shaft(self) -> 'float':
        """float: 'ExcitationOrderAsRotationalOrderOfShaft' is the original name of this property."""

        temp = self.wrapped.ExcitationOrderAsRotationalOrderOfShaft

        if temp is None:
            return None

        return temp

    @excitation_order_as_rotational_order_of_shaft.setter
    def excitation_order_as_rotational_order_of_shaft(self, value: 'float'):
        self.wrapped.ExcitationOrderAsRotationalOrderOfShaft = float(value) if value else 0.0

    @property
    def mean_value(self) -> 'float':
        """float: 'MeanValue' is the original name of this property."""

        temp = self.wrapped.MeanValue

        if temp is None:
            return None

        return temp

    @mean_value.setter
    def mean_value(self, value: 'float'):
        self.wrapped.MeanValue = float(value) if value else 0.0

    @property
    def number_of_cycles_in_signal(self) -> 'float':
        """float: 'NumberOfCyclesInSignal' is the original name of this property."""

        temp = self.wrapped.NumberOfCyclesInSignal

        if temp is None:
            return None

        return temp

    @number_of_cycles_in_signal.setter
    def number_of_cycles_in_signal(self, value: 'float'):
        self.wrapped.NumberOfCyclesInSignal = float(value) if value else 0.0

    @property
    def number_of_harmonics(self) -> 'int':
        """int: 'NumberOfHarmonics' is the original name of this property."""

        temp = self.wrapped.NumberOfHarmonics

        if temp is None:
            return None

        return temp

    @number_of_harmonics.setter
    def number_of_harmonics(self, value: 'int'):
        self.wrapped.NumberOfHarmonics = int(value) if value else 0

    @property
    def number_of_values(self) -> 'int':
        """int: 'NumberOfValues' is the original name of this property."""

        temp = self.wrapped.NumberOfValues

        if temp is None:
            return None

        return temp

    @number_of_values.setter
    def number_of_values(self, value: 'int'):
        self.wrapped.NumberOfValues = int(value) if value else 0

    @property
    def peak_to_peak(self) -> 'float':
        """float: 'PeakToPeak' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeakToPeak

        if temp is None:
            return None

        return temp

    @property
    def excitations(self) -> 'List[_1320.FourierSeries]':
        """List[FourierSeries]: 'Excitations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Excitations

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

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

    def clear_all_data(self):
        """ 'ClearAllData' is the original name of this method."""

        self.wrapped.ClearAllData()

    def clear_selected_data(self):
        """ 'ClearSelectedData' is the original name of this method."""

        self.wrapped.ClearSelectedData()

    def set_selected_harmonic_load_data(self, fourier_series_values: 'List[float]', fourier_series_name: 'str', fourier_series_measurement_type: '_7286.MeasurementType'):
        """ 'SetSelectedHarmonicLoadData' is the original name of this method.

        Args:
            fourier_series_values (List[float])
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """

        fourier_series_values = conversion.mp_to_pn_array_float(fourier_series_values)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(fourier_series_measurement_type)
        self.wrapped.SetSelectedHarmonicLoadData.Overloads[_ARRAY[_DOUBLE], _STRING, _MEASUREMENT_TYPE](fourier_series_values, fourier_series_name if fourier_series_name else '', fourier_series_measurement_type)

    def set_selected_harmonic_load_data_extended(self, amplitudes: 'List[float]', phases: 'List[float]', mean_value: 'float', fourier_series_name: 'str', fourier_series_measurement_type: '_7286.MeasurementType'):
        """ 'SetSelectedHarmonicLoadData' is the original name of this method.

        Args:
            amplitudes (List[float])
            phases (List[float])
            mean_value (float)
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """

        amplitudes = conversion.mp_to_pn_list_float(amplitudes)
        phases = conversion.mp_to_pn_list_float(phases)
        mean_value = float(mean_value)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(fourier_series_measurement_type)
        self.wrapped.SetSelectedHarmonicLoadData.Overloads[_LIST[_DOUBLE], _LIST[_DOUBLE], _DOUBLE, _STRING, _MEASUREMENT_TYPE](amplitudes, phases, mean_value if mean_value else 0.0, fourier_series_name if fourier_series_name else '', fourier_series_measurement_type)

    def set_selected_harmonic_load_data_with_fourier_series(self, fourier_series: '_1320.FourierSeries'):
        """ 'SetSelectedHarmonicLoadData' is the original name of this method.

        Args:
            fourier_series (mastapy.math_utility.FourierSeries)
        """

        self.wrapped.SetSelectedHarmonicLoadData.Overloads[_FOURIER_SERIES](fourier_series.wrapped if fourier_series else None)

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
