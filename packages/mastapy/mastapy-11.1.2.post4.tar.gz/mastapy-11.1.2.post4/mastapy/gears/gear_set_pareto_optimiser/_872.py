"""_872.py

DesignSpaceSearchBase
"""


from typing import List, Generic, TypeVar

from mastapy._internal.python_net import python_net_import
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears.gear_set_pareto_optimiser import (
    _869, _881, _870, _888,
    _903, _906
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.math_utility.optimisation import _1356, _1353, _1347
from mastapy import _0
from mastapy.gears.analysis import _1169

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_DESIGN_SPACE_SEARCH_BASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'DesignSpaceSearchBase')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignSpaceSearchBase',)


TAnalysis = TypeVar('TAnalysis', bound='_1169.AbstractGearSetAnalysis')
TCandidate = TypeVar('TCandidate')


class DesignSpaceSearchBase(_0.APIBase, Generic[TAnalysis, TCandidate]):
    """DesignSpaceSearchBase

    This is a mastapy class.

    Generic Types:
        TAnalysis
        TCandidate
    """

    TYPE = _DESIGN_SPACE_SEARCH_BASE

    def __init__(self, instance_to_wrap: 'DesignSpaceSearchBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design_space_search_strategy_database(self) -> 'str':
        """str: 'DesignSpaceSearchStrategyDatabase' is the original name of this property."""

        temp = self.wrapped.DesignSpaceSearchStrategyDatabase.SelectedItemName

        if temp is None:
            return None

        return temp

    @design_space_search_strategy_database.setter
    def design_space_search_strategy_database(self, value: 'str'):
        self.wrapped.DesignSpaceSearchStrategyDatabase.SetSelectedItem(str(value) if value else '')

    @property
    def design_space_search_strategy_database_duty_cycle(self) -> 'str':
        """str: 'DesignSpaceSearchStrategyDatabaseDutyCycle' is the original name of this property."""

        temp = self.wrapped.DesignSpaceSearchStrategyDatabaseDutyCycle.SelectedItemName

        if temp is None:
            return None

        return temp

    @design_space_search_strategy_database_duty_cycle.setter
    def design_space_search_strategy_database_duty_cycle(self, value: 'str'):
        self.wrapped.DesignSpaceSearchStrategyDatabaseDutyCycle.SetSelectedItem(str(value) if value else '')

    @property
    def display_candidates(self) -> 'enum_with_selected_value.EnumWithSelectedValue_CandidateDisplayChoice':
        """enum_with_selected_value.EnumWithSelectedValue_CandidateDisplayChoice: 'DisplayCandidates' is the original name of this property."""

        temp = self.wrapped.DisplayCandidates

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CandidateDisplayChoice.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @display_candidates.setter
    def display_candidates(self, value: 'enum_with_selected_value.EnumWithSelectedValue_CandidateDisplayChoice.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CandidateDisplayChoice.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DisplayCandidates = value

    @property
    def maximum_number_of_candidates_to_display(self) -> 'int':
        """int: 'MaximumNumberOfCandidatesToDisplay' is the original name of this property."""

        temp = self.wrapped.MaximumNumberOfCandidatesToDisplay

        if temp is None:
            return None

        return temp

    @maximum_number_of_candidates_to_display.setter
    def maximum_number_of_candidates_to_display(self, value: 'int'):
        self.wrapped.MaximumNumberOfCandidatesToDisplay = int(value) if value else 0

    @property
    def number_of_candidates_after_filtering(self) -> 'int':
        """int: 'NumberOfCandidatesAfterFiltering' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfCandidatesAfterFiltering

        if temp is None:
            return None

        return temp

    @property
    def number_of_dominant_candidates(self) -> 'int':
        """int: 'NumberOfDominantCandidates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfDominantCandidates

        if temp is None:
            return None

        return temp

    @property
    def number_of_feasible_candidates(self) -> 'int':
        """int: 'NumberOfFeasibleCandidates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfFeasibleCandidates

        if temp is None:
            return None

        return temp

    @property
    def number_of_unfiltered_candidates(self) -> 'int':
        """int: 'NumberOfUnfilteredCandidates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfUnfilteredCandidates

        if temp is None:
            return None

        return temp

    @property
    def number_of_unrateable_designs(self) -> 'int':
        """int: 'NumberOfUnrateableDesigns' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfUnrateableDesigns

        if temp is None:
            return None

        return temp

    @property
    def remove_candidates_with(self) -> '_881.LargerOrSmaller':
        """LargerOrSmaller: 'RemoveCandidatesWith' is the original name of this property."""

        temp = self.wrapped.RemoveCandidatesWith

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_881.LargerOrSmaller)(value) if value is not None else None

    @remove_candidates_with.setter
    def remove_candidates_with(self, value: '_881.LargerOrSmaller'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RemoveCandidatesWith = value

    @property
    def reporting_string_for_too_many_candidates_to_be_evaluated(self) -> 'str':
        """str: 'ReportingStringForTooManyCandidatesToBeEvaluated' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportingStringForTooManyCandidatesToBeEvaluated

        if temp is None:
            return None

        return temp

    @property
    def selected_points(self) -> 'List[int]':
        """List[int]: 'SelectedPoints' is the original name of this property."""

        temp = self.wrapped.SelectedPoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)
        return value

    @selected_points.setter
    def selected_points(self, value: 'List[int]'):
        value = value if value else None
        value = conversion.mp_to_pn_objects_in_list(value)
        self.wrapped.SelectedPoints = value

    @property
    def total_number_of_candidates_to_be_evaluated(self) -> 'int':
        """int: 'TotalNumberOfCandidatesToBeEvaluated' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalNumberOfCandidatesToBeEvaluated

        if temp is None:
            return None

        return temp

    @property
    def viewing_candidates_selected_in_chart(self) -> 'bool':
        """bool: 'ViewingCandidatesSelectedInChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ViewingCandidatesSelectedInChart

        if temp is None:
            return None

        return temp

    @property
    def load_case_duty_cycle(self) -> 'TAnalysis':
        """TAnalysis: 'LoadCaseDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadCaseDutyCycle

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate(self) -> 'TAnalysis':
        """TAnalysis: 'SelectedCandidate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidate

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_design_space_search_strategy(self) -> '_1356.ParetoOptimisationStrategy':
        """ParetoOptimisationStrategy: 'SelectedDesignSpaceSearchStrategy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedDesignSpaceSearchStrategy

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def all_candidate_designs_including_original_design(self) -> 'List[TCandidate]':
        """List[TCandidate]: 'AllCandidateDesignsIncludingOriginalDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllCandidateDesignsIncludingOriginalDesign

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def all_candidate_designs_to_display(self) -> 'List[TCandidate]':
        """List[TCandidate]: 'AllCandidateDesignsToDisplay' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllCandidateDesignsToDisplay

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def all_candidate_designs_to_display_without_original_design(self) -> 'List[TCandidate]':
        """List[TCandidate]: 'AllCandidateDesignsToDisplayWithoutOriginalDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllCandidateDesignsToDisplayWithoutOriginalDesign

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def candidate_designs_to_display(self) -> 'List[TCandidate]':
        """List[TCandidate]: 'CandidateDesignsToDisplay' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CandidateDesignsToDisplay

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def chart_details(self) -> 'List[_870.ChartInfoBase[TAnalysis, TCandidate]]':
        """List[ChartInfoBase[TAnalysis, TCandidate]]: 'ChartDetails' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ChartDetails

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def filters(self) -> 'List[_1353.ParetoOptimisationFilter]':
        """List[ParetoOptimisationFilter]: 'Filters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Filters

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def input_setters(self) -> 'List[_1347.InputSetter[TAnalysis]]':
        """List[InputSetter[TAnalysis]]: 'InputSetters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InputSetters

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def optimisation_targets(self) -> 'List[_888.OptimisationTarget[TAnalysis]]':
        """List[OptimisationTarget[TAnalysis]]: 'OptimisationTargets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OptimisationTargets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def reasons_for_invalid_candidates(self) -> 'List[_903.ReasonsForInvalidDesigns]':
        """List[ReasonsForInvalidDesigns]: 'ReasonsForInvalidCandidates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReasonsForInvalidCandidates

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def table_filters(self) -> 'List[_906.TableFilter[TAnalysis, TCandidate]]':
        """List[TableFilter[TAnalysis, TCandidate]]: 'TableFilters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TableFilters

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

    def add_table_filter(self):
        """ 'AddTableFilter' is the original name of this method."""

        self.wrapped.AddTableFilter()

    def find_dominant_candidates(self):
        """ 'FindDominantCandidates' is the original name of this method."""

        self.wrapped.FindDominantCandidates()

    def load_strategy(self):
        """ 'LoadStrategy' is the original name of this method."""

        self.wrapped.LoadStrategy()

    def save_results(self):
        """ 'SaveResults' is the original name of this method."""

        self.wrapped.SaveResults()

    def save_strategy(self):
        """ 'SaveStrategy' is the original name of this method."""

        self.wrapped.SaveStrategy()

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
