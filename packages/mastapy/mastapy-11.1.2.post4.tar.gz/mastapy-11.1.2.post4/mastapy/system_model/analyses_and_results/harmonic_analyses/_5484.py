"""_5484.py

FrequencyOptionsForHarmonicAnalysisResults
"""


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.analysis_cases import _7262
from mastapy.system_model.analyses_and_results.static_loads import _6528
from mastapy._internal.python_net import python_net_import

_FREQUENCY_OPTIONS_FOR_HARMONIC_ANALYSIS_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'FrequencyOptionsForHarmonicAnalysisResults')


__docformat__ = 'restructuredtext en'
__all__ = ('FrequencyOptionsForHarmonicAnalysisResults',)


class FrequencyOptionsForHarmonicAnalysisResults(_7262.AbstractAnalysisOptions['_6528.StaticLoadCase']):
    """FrequencyOptionsForHarmonicAnalysisResults

    This is a mastapy class.
    """

    TYPE = _FREQUENCY_OPTIONS_FOR_HARMONIC_ANALYSIS_RESULTS

    def __init__(self, instance_to_wrap: 'FrequencyOptionsForHarmonicAnalysisResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def base_points_on_mode_frequencies(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'BasePointsOnModeFrequencies' is the original name of this property."""

        temp = self.wrapped.BasePointsOnModeFrequencies

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @base_points_on_mode_frequencies.setter
    def base_points_on_mode_frequencies(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.BasePointsOnModeFrequencies = value

    @property
    def clustering_bias_of_additional_points(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ClusteringBiasOfAdditionalPoints' is the original name of this property."""

        temp = self.wrapped.ClusteringBiasOfAdditionalPoints

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @clustering_bias_of_additional_points.setter
    def clustering_bias_of_additional_points(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ClusteringBiasOfAdditionalPoints = value

    @property
    def logarithmic_frequency_axis(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'LogarithmicFrequencyAxis' is the original name of this property."""

        temp = self.wrapped.LogarithmicFrequencyAxis

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @logarithmic_frequency_axis.setter
    def logarithmic_frequency_axis(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.LogarithmicFrequencyAxis = value

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
    def minimum(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Minimum' is the original name of this property."""

        temp = self.wrapped.Minimum

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minimum.setter
    def minimum(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Minimum = value

    @property
    def number_of_points_across_range(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfPointsAcrossRange' is the original name of this property."""

        temp = self.wrapped.NumberOfPointsAcrossRange

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_points_across_range.setter
    def number_of_points_across_range(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfPointsAcrossRange = value

    @property
    def use_logarithmic_spacing(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'UseLogarithmicSpacing' is the original name of this property."""

        temp = self.wrapped.UseLogarithmicSpacing

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @use_logarithmic_spacing.setter
    def use_logarithmic_spacing(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.UseLogarithmicSpacing = value

    @property
    def design_defaults(self) -> 'FrequencyOptionsForHarmonicAnalysisResults':
        """FrequencyOptionsForHarmonicAnalysisResults: 'DesignDefaults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DesignDefaults

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
