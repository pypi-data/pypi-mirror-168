"""_870.py

ChartInfoBase
"""


from typing import List, Generic, TypeVar

from PIL.Image import Image

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.utility.reporting_property_framework import _1568
from mastapy.math_utility.optimisation import _1358
from mastapy.gears.gear_set_pareto_optimiser import (
    _872, _871, _874, _878,
    _879, _882, _885, _904,
    _905, _868, _880
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy.gears.analysis import _1169
from mastapy._internal.python_net import python_net_import

_CHART_INFO_BASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'ChartInfoBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ChartInfoBase',)


TAnalysis = TypeVar('TAnalysis', bound='_1169.AbstractGearSetAnalysis')
TCandidate = TypeVar('TCandidate')


class ChartInfoBase(_0.APIBase, Generic[TAnalysis, TCandidate]):
    """ChartInfoBase

    This is a mastapy class.

    Generic Types:
        TAnalysis
        TCandidate
    """

    TYPE = _CHART_INFO_BASE

    def __init__(self, instance_to_wrap: 'ChartInfoBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def chart_name(self) -> 'str':
        """str: 'ChartName' is the original name of this property."""

        temp = self.wrapped.ChartName

        if temp is None:
            return None

        return temp

    @chart_name.setter
    def chart_name(self, value: 'str'):
        self.wrapped.ChartName = str(value) if value else ''

    @property
    def chart_type(self) -> '_1568.CustomChartType':
        """CustomChartType: 'ChartType' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ChartType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1568.CustomChartType)(value) if value is not None else None

    @property
    def result_chart_bar_and_line(self) -> 'Image':
        """Image: 'ResultChartBarAndLine' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResultChartBarAndLine

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def result_chart_scatter(self) -> 'Image':
        """Image: 'ResultChartScatter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResultChartScatter

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def select_chart_type(self) -> '_1358.ParetoOptimisationStrategyChartInformation.ScatterOrBarChart':
        """ParetoOptimisationStrategyChartInformation.ScatterOrBarChart: 'SelectChartType' is the original name of this property."""

        temp = self.wrapped.SelectChartType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1358.ParetoOptimisationStrategyChartInformation.ScatterOrBarChart)(value) if value is not None else None

    @select_chart_type.setter
    def select_chart_type(self, value: '_1358.ParetoOptimisationStrategyChartInformation.ScatterOrBarChart'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SelectChartType = value

    @property
    def selected_candidate_design(self) -> 'int':
        """int: 'SelectedCandidateDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateDesign

        if temp is None:
            return None

        return temp

    @property
    def optimiser(self) -> '_872.DesignSpaceSearchBase[TAnalysis, TCandidate]':
        """DesignSpaceSearchBase[TAnalysis, TCandidate]: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Optimiser

        if temp is None:
            return None

        if _872.DesignSpaceSearchBase[TAnalysis, TCandidate].TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast optimiser to DesignSpaceSearchBase[TAnalysis, TCandidate]. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[TAnalysis, TCandidate](temp) if temp is not None else None

    @property
    def optimiser_of_type_cylindrical_gear_set_pareto_optimiser(self) -> '_871.CylindricalGearSetParetoOptimiser':
        """CylindricalGearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Optimiser

        if temp is None:
            return None

        if _871.CylindricalGearSetParetoOptimiser.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast optimiser to CylindricalGearSetParetoOptimiser. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def optimiser_of_type_face_gear_set_pareto_optimiser(self) -> '_874.FaceGearSetParetoOptimiser':
        """FaceGearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Optimiser

        if temp is None:
            return None

        if _874.FaceGearSetParetoOptimiser.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast optimiser to FaceGearSetParetoOptimiser. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def optimiser_of_type_gear_set_pareto_optimiser(self) -> '_878.GearSetParetoOptimiser':
        """GearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Optimiser

        if temp is None:
            return None

        if _878.GearSetParetoOptimiser.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast optimiser to GearSetParetoOptimiser. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def optimiser_of_type_hypoid_gear_set_pareto_optimiser(self) -> '_879.HypoidGearSetParetoOptimiser':
        """HypoidGearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Optimiser

        if temp is None:
            return None

        if _879.HypoidGearSetParetoOptimiser.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast optimiser to HypoidGearSetParetoOptimiser. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def optimiser_of_type_micro_geometry_design_space_search(self) -> '_882.MicroGeometryDesignSpaceSearch':
        """MicroGeometryDesignSpaceSearch: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Optimiser

        if temp is None:
            return None

        if _882.MicroGeometryDesignSpaceSearch.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast optimiser to MicroGeometryDesignSpaceSearch. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def optimiser_of_type_micro_geometry_gear_set_design_space_search(self) -> '_885.MicroGeometryGearSetDesignSpaceSearch':
        """MicroGeometryGearSetDesignSpaceSearch: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Optimiser

        if temp is None:
            return None

        if _885.MicroGeometryGearSetDesignSpaceSearch.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast optimiser to MicroGeometryGearSetDesignSpaceSearch. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def optimiser_of_type_spiral_bevel_gear_set_pareto_optimiser(self) -> '_904.SpiralBevelGearSetParetoOptimiser':
        """SpiralBevelGearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Optimiser

        if temp is None:
            return None

        if _904.SpiralBevelGearSetParetoOptimiser.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast optimiser to SpiralBevelGearSetParetoOptimiser. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def optimiser_of_type_straight_bevel_gear_set_pareto_optimiser(self) -> '_905.StraightBevelGearSetParetoOptimiser':
        """StraightBevelGearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Optimiser

        if temp is None:
            return None

        if _905.StraightBevelGearSetParetoOptimiser.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast optimiser to StraightBevelGearSetParetoOptimiser. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bars(self) -> 'List[_868.BarForPareto[TAnalysis, TCandidate]]':
        """List[BarForPareto[TAnalysis, TCandidate]]: 'Bars' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bars

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def input_sliders(self) -> 'List[_880.InputSliderForPareto[TAnalysis, TCandidate]]':
        """List[InputSliderForPareto[TAnalysis, TCandidate]]: 'InputSliders' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InputSliders

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

    def add_bar(self):
        """ 'AddBar' is the original name of this method."""

        self.wrapped.AddBar()

    def add_selected_design(self):
        """ 'AddSelectedDesign' is the original name of this method."""

        self.wrapped.AddSelectedDesign()

    def add_selected_designs(self):
        """ 'AddSelectedDesigns' is the original name of this method."""

        self.wrapped.AddSelectedDesigns()

    def remove_chart(self):
        """ 'RemoveChart' is the original name of this method."""

        self.wrapped.RemoveChart()

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
