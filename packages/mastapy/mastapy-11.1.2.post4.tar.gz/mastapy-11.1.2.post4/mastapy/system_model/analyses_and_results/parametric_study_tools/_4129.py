"""_4129.py

ParametricStudyToolOptions
"""


from typing import List

from mastapy._internal.implicit import enum_with_selected_value, overridable, list_with_selected_item
from mastapy.system_model.analyses_and_results.static_loads import _6541, _6654
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.system_model import _1964, _1960
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4131, _4132
from mastapy.system_model.analyses_and_results import _2397
from mastapy.math_utility.convergence import _1380
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PARAMETRIC_STUDY_TOOL_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ParametricStudyToolOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyToolOptions',)


class ParametricStudyToolOptions(_0.APIBase):
    """ParametricStudyToolOptions

    This is a mastapy class.
    """

    TYPE = _PARAMETRIC_STUDY_TOOL_OPTIONS

    def __init__(self, instance_to_wrap: 'ParametricStudyToolOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def analysis_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_AnalysisType':
        """enum_with_selected_value.EnumWithSelectedValue_AnalysisType: 'AnalysisType' is the original name of this property."""

        temp = self.wrapped.AnalysisType

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_AnalysisType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @analysis_type.setter
    def analysis_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_AnalysisType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_AnalysisType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.AnalysisType = value

    @property
    def changing_design(self) -> 'bool':
        """bool: 'ChangingDesign' is the original name of this property."""

        temp = self.wrapped.ChangingDesign

        if temp is None:
            return None

        return temp

    @changing_design.setter
    def changing_design(self, value: 'bool'):
        self.wrapped.ChangingDesign = bool(value) if value else False

    @property
    def folder_path_for_saved_files(self) -> 'str':
        """str: 'FolderPathForSavedFiles' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FolderPathForSavedFiles

        if temp is None:
            return None

        return temp

    @property
    def is_logging_data(self) -> 'bool':
        """bool: 'IsLoggingData' is the original name of this property."""

        temp = self.wrapped.IsLoggingData

        if temp is None:
            return None

        return temp

    @is_logging_data.setter
    def is_logging_data(self, value: 'bool'):
        self.wrapped.IsLoggingData = bool(value) if value else False

    @property
    def log_report(self) -> 'bool':
        """bool: 'LogReport' is the original name of this property."""

        temp = self.wrapped.LogReport

        if temp is None:
            return None

        return temp

    @log_report.setter
    def log_report(self, value: 'bool'):
        self.wrapped.LogReport = bool(value) if value else False

    @property
    def maximum_number_of_design_copies_to_use(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'MaximumNumberOfDesignCopiesToUse' is the original name of this property."""

        temp = self.wrapped.MaximumNumberOfDesignCopiesToUse

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @maximum_number_of_design_copies_to_use.setter
    def maximum_number_of_design_copies_to_use(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.MaximumNumberOfDesignCopiesToUse = value

    @property
    def number_of_analysis_dimensions(self) -> 'int':
        """int: 'NumberOfAnalysisDimensions' is the original name of this property."""

        temp = self.wrapped.NumberOfAnalysisDimensions

        if temp is None:
            return None

        return temp

    @number_of_analysis_dimensions.setter
    def number_of_analysis_dimensions(self, value: 'int'):
        self.wrapped.NumberOfAnalysisDimensions = int(value) if value else 0

    @property
    def number_of_steps(self) -> 'int':
        """int: 'NumberOfSteps' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfSteps

        if temp is None:
            return None

        return temp

    @property
    def parametric_study_type(self) -> '_6654.ParametricStudyType':
        """ParametricStudyType: 'ParametricStudyType' is the original name of this property."""

        temp = self.wrapped.ParametricStudyType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_6654.ParametricStudyType)(value) if value is not None else None

    @parametric_study_type.setter
    def parametric_study_type(self, value: '_6654.ParametricStudyType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ParametricStudyType = value

    @property
    def perform_system_optimisation_pst_post_analysis(self) -> 'bool':
        """bool: 'PerformSystemOptimisationPSTPostAnalysis' is the original name of this property."""

        temp = self.wrapped.PerformSystemOptimisationPSTPostAnalysis

        if temp is None:
            return None

        return temp

    @perform_system_optimisation_pst_post_analysis.setter
    def perform_system_optimisation_pst_post_analysis(self, value: 'bool'):
        self.wrapped.PerformSystemOptimisationPSTPostAnalysis = bool(value) if value else False

    @property
    def put_newly_added_numerical_variables_into(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'PutNewlyAddedNumericalVariablesInto' is the original name of this property."""

        temp = self.wrapped.PutNewlyAddedNumericalVariablesInto

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @put_newly_added_numerical_variables_into.setter
    def put_newly_added_numerical_variables_into(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.PutNewlyAddedNumericalVariablesInto = value

    @property
    def save_design_at_each_step(self) -> 'bool':
        """bool: 'SaveDesignAtEachStep' is the original name of this property."""

        temp = self.wrapped.SaveDesignAtEachStep

        if temp is None:
            return None

        return temp

    @save_design_at_each_step.setter
    def save_design_at_each_step(self, value: 'bool'):
        self.wrapped.SaveDesignAtEachStep = bool(value) if value else False

    @property
    def steps_for_statistical_study(self) -> 'int':
        """int: 'StepsForStatisticalStudy' is the original name of this property."""

        temp = self.wrapped.StepsForStatisticalStudy

        if temp is None:
            return None

        return temp

    @steps_for_statistical_study.setter
    def steps_for_statistical_study(self, value: 'int'):
        self.wrapped.StepsForStatisticalStudy = int(value) if value else 0

    @property
    def steps_in_dimension_1(self) -> 'int':
        """int: 'StepsInDimension1' is the original name of this property."""

        temp = self.wrapped.StepsInDimension1

        if temp is None:
            return None

        return temp

    @steps_in_dimension_1.setter
    def steps_in_dimension_1(self, value: 'int'):
        self.wrapped.StepsInDimension1 = int(value) if value else 0

    @property
    def steps_in_dimension_2(self) -> 'int':
        """int: 'StepsInDimension2' is the original name of this property."""

        temp = self.wrapped.StepsInDimension2

        if temp is None:
            return None

        return temp

    @steps_in_dimension_2.setter
    def steps_in_dimension_2(self, value: 'int'):
        self.wrapped.StepsInDimension2 = int(value) if value else 0

    @property
    def use_multiple_designs(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'UseMultipleDesigns' is the original name of this property."""

        temp = self.wrapped.UseMultipleDesigns

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @use_multiple_designs.setter
    def use_multiple_designs(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.UseMultipleDesigns = value

    @property
    def external_full_fe_loader(self) -> '_1964.ExternalFullFELoader':
        """ExternalFullFELoader: 'ExternalFullFELoader' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExternalFullFELoader

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def step_results(self) -> 'List[_4131.ParametricStudyToolStepResult]':
        """List[ParametricStudyToolStepResult]: 'StepResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StepResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def study_variables(self) -> 'List[_4132.ParametricStudyVariable]':
        """List[ParametricStudyVariable]: 'StudyVariables' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StudyVariables

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def parametric_study_logging_variables(self) -> 'List[_2397.AnalysisCaseVariable]':
        """List[AnalysisCaseVariable]: 'ParametricStudyLoggingVariables' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParametricStudyLoggingVariables

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

    def edit_folder_path(self):
        """ 'EditFolderPath' is the original name of this method."""

        self.wrapped.EditFolderPath()

    def add_logging_variable(self, design_entity: '_1960.DesignEntity', path: 'List[str]') -> '_2397.AnalysisCaseVariable':
        """ 'AddLoggingVariable' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.DesignEntity)
            path (List[str])

        Returns:
            mastapy.system_model.analyses_and_results.AnalysisCaseVariable
        """

        path = conversion.to_list_any(path)
        method_result = self.wrapped.AddLoggingVariable(design_entity.wrapped if design_entity else None, path)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def add_study_variable(self, design_entity: '_1960.DesignEntity', path: 'List[str]') -> '_4132.ParametricStudyVariable':
        """ 'AddStudyVariable' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.DesignEntity)
            path (List[str])

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyVariable
        """

        path = conversion.to_list_any(path)
        method_result = self.wrapped.AddStudyVariable(design_entity.wrapped if design_entity else None, path)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def data_logger_for(self, design_entity: '_1960.DesignEntity') -> '_1380.DataLogger':
        """ 'DataLoggerFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.DesignEntity)

        Returns:
            mastapy.math_utility.convergence.DataLogger
        """

        method_result = self.wrapped.DataLoggerFor(design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def move_study_variable_down(self, study_variable: '_4132.ParametricStudyVariable'):
        """ 'MoveStudyVariableDown' is the original name of this method.

        Args:
            study_variable (mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyVariable)
        """

        self.wrapped.MoveStudyVariableDown(study_variable.wrapped if study_variable else None)

    def move_study_variable_up(self, study_variable: '_4132.ParametricStudyVariable'):
        """ 'MoveStudyVariableUp' is the original name of this method.

        Args:
            study_variable (mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyVariable)
        """

        self.wrapped.MoveStudyVariableUp(study_variable.wrapped if study_variable else None)

    def remove_logging_variable(self, analysis_variable: '_2397.AnalysisCaseVariable'):
        """ 'RemoveLoggingVariable' is the original name of this method.

        Args:
            analysis_variable (mastapy.system_model.analyses_and_results.AnalysisCaseVariable)
        """

        self.wrapped.RemoveLoggingVariable(analysis_variable.wrapped if analysis_variable else None)

    def remove_study_variable(self, study_variable: '_4132.ParametricStudyVariable'):
        """ 'RemoveStudyVariable' is the original name of this method.

        Args:
            study_variable (mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyVariable)
        """

        self.wrapped.RemoveStudyVariable(study_variable.wrapped if study_variable else None)

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
