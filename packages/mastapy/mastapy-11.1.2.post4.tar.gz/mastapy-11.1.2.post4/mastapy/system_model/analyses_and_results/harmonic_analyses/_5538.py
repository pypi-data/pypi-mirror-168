"""_5538.py

SpeedOptionsForHarmonicAnalysisResults
"""


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.analysis_cases import _7262
from mastapy.system_model.analyses_and_results.static_loads import _6528
from mastapy._internal.python_net import python_net_import

_SPEED_OPTIONS_FOR_HARMONIC_ANALYSIS_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'SpeedOptionsForHarmonicAnalysisResults')


__docformat__ = 'restructuredtext en'
__all__ = ('SpeedOptionsForHarmonicAnalysisResults',)


class SpeedOptionsForHarmonicAnalysisResults(_7262.AbstractAnalysisOptions['_6528.StaticLoadCase']):
    """SpeedOptionsForHarmonicAnalysisResults

    This is a mastapy class.
    """

    TYPE = _SPEED_OPTIONS_FOR_HARMONIC_ANALYSIS_RESULTS

    def __init__(self, instance_to_wrap: 'SpeedOptionsForHarmonicAnalysisResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Maximum' is the original name of this property."""

        temp = self.wrapped.Maximum

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @maximum.setter
    def maximum(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Maximum = value

    @property
    def minimum(self) -> 'float':
        """float: 'Minimum' is the original name of this property."""

        temp = self.wrapped.Minimum

        if temp is None:
            return None

        return temp

    @minimum.setter
    def minimum(self, value: 'float'):
        self.wrapped.Minimum = float(value) if value else 0.0

    @property
    def number_of_speeds(self) -> 'int':
        """int: 'NumberOfSpeeds' is the original name of this property."""

        temp = self.wrapped.NumberOfSpeeds

        if temp is None:
            return None

        return temp

    @number_of_speeds.setter
    def number_of_speeds(self, value: 'int'):
        self.wrapped.NumberOfSpeeds = int(value) if value else 0

    @property
    def reference_power_load_speed(self) -> 'float':
        """float: 'ReferencePowerLoadSpeed' is the original name of this property."""

        temp = self.wrapped.ReferencePowerLoadSpeed

        if temp is None:
            return None

        return temp

    @reference_power_load_speed.setter
    def reference_power_load_speed(self, value: 'float'):
        self.wrapped.ReferencePowerLoadSpeed = float(value) if value else 0.0

    @property
    def show_result_in_time_domain(self) -> 'bool':
        """bool: 'ShowResultInTimeDomain' is the original name of this property."""

        temp = self.wrapped.ShowResultInTimeDomain

        if temp is None:
            return None

        return temp

    @show_result_in_time_domain.setter
    def show_result_in_time_domain(self, value: 'bool'):
        self.wrapped.ShowResultInTimeDomain = bool(value) if value else False

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
