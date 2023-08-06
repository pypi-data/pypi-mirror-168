"""_4090.py

DutyCycleResultsForAllComponents
"""


from typing import List

from mastapy.system_model.analyses_and_results.parametric_study_tools import (
    _4091, _4092, _4093, _4094
)
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_RESULTS_FOR_ALL_COMPONENTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'DutyCycleResultsForAllComponents')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycleResultsForAllComponents',)


class DutyCycleResultsForAllComponents(_0.APIBase):
    """DutyCycleResultsForAllComponents

    This is a mastapy class.
    """

    TYPE = _DUTY_CYCLE_RESULTS_FOR_ALL_COMPONENTS

    def __init__(self, instance_to_wrap: 'DutyCycleResultsForAllComponents.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def results_for_all_gear_sets(self) -> '_4091.DutyCycleResultsForAllGearSets':
        """DutyCycleResultsForAllGearSets: 'ResultsForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResultsForAllGearSets

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def results_for_root_assembly(self) -> '_4092.DutyCycleResultsForRootAssembly':
        """DutyCycleResultsForRootAssembly: 'ResultsForRootAssembly' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResultsForRootAssembly

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def results_for_all_bearings(self) -> 'List[_4093.DutyCycleResultsForSingleBearing]':
        """List[DutyCycleResultsForSingleBearing]: 'ResultsForAllBearings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResultsForAllBearings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def results_for_all_shafts(self) -> 'List[_4094.DutyCycleResultsForSingleShaft]':
        """List[DutyCycleResultsForSingleShaft]: 'ResultsForAllShafts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResultsForAllShafts

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
