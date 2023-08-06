"""_1561.py

DynamicCustomReportItem
"""


from mastapy._internal import constructor
from mastapy.utility.report import (
    _1542, _1524, _1530, _1531,
    _1532, _1533, _1534, _1535,
    _1537, _1538, _1539, _1540,
    _1541, _1543, _1545, _1546,
    _1549, _1550, _1551, _1553,
    _1554, _1555, _1556, _1558,
    _1559
)
from mastapy.shafts import _20
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical import _995
from mastapy.utility_gui.charts import _1626, _1627
from mastapy.bearings.bearing_results import (
    _1709, _1710, _1713, _1721
)
from mastapy.system_model.analyses_and_results.system_deflections.reporting import _2593
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4126
from mastapy.system_model.analyses_and_results.modal_analyses.reporting import _4454, _4458
from mastapy._internal.python_net import python_net_import

_DYNAMIC_CUSTOM_REPORT_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'DynamicCustomReportItem')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicCustomReportItem',)


class DynamicCustomReportItem(_1550.CustomReportNameableItem):
    """DynamicCustomReportItem

    This is a mastapy class.
    """

    TYPE = _DYNAMIC_CUSTOM_REPORT_ITEM

    def __init__(self, instance_to_wrap: 'DynamicCustomReportItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_main_report_item(self) -> 'bool':
        """bool: 'IsMainReportItem' is the original name of this property."""

        temp = self.wrapped.IsMainReportItem

        if temp is None:
            return None

        return temp

    @is_main_report_item.setter
    def is_main_report_item(self, value: 'bool'):
        self.wrapped.IsMainReportItem = bool(value) if value else False

    @property
    def inner_item(self) -> '_1542.CustomReportItem':
        """CustomReportItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1542.CustomReportItem.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItem. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_shaft_damage_results_table_and_chart(self) -> '_20.ShaftDamageResultsTableAndChart':
        """ShaftDamageResultsTableAndChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _20.ShaftDamageResultsTableAndChart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ShaftDamageResultsTableAndChart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_cylindrical_gear_table_with_mg_charts(self) -> '_995.CylindricalGearTableWithMGCharts':
        """CylindricalGearTableWithMGCharts: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _995.CylindricalGearTableWithMGCharts.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CylindricalGearTableWithMGCharts. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_ad_hoc_custom_table(self) -> '_1524.AdHocCustomTable':
        """AdHocCustomTable: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1524.AdHocCustomTable.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to AdHocCustomTable. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_chart(self) -> '_1530.CustomChart':
        """CustomChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1530.CustomChart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomChart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_graphic(self) -> '_1531.CustomGraphic':
        """CustomGraphic: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1531.CustomGraphic.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomGraphic. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_image(self) -> '_1532.CustomImage':
        """CustomImage: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1532.CustomImage.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomImage. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report(self) -> '_1533.CustomReport':
        """CustomReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1533.CustomReport.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReport. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_cad_drawing(self) -> '_1534.CustomReportCadDrawing':
        """CustomReportCadDrawing: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1534.CustomReportCadDrawing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportCadDrawing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_chart(self) -> '_1535.CustomReportChart':
        """CustomReportChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1535.CustomReportChart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportChart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_column(self) -> '_1537.CustomReportColumn':
        """CustomReportColumn: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1537.CustomReportColumn.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportColumn. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_columns(self) -> '_1538.CustomReportColumns':
        """CustomReportColumns: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1538.CustomReportColumns.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportColumns. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_definition_item(self) -> '_1539.CustomReportDefinitionItem':
        """CustomReportDefinitionItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1539.CustomReportDefinitionItem.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportDefinitionItem. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_horizontal_line(self) -> '_1540.CustomReportHorizontalLine':
        """CustomReportHorizontalLine: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1540.CustomReportHorizontalLine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportHorizontalLine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_html_item(self) -> '_1541.CustomReportHtmlItem':
        """CustomReportHtmlItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1541.CustomReportHtmlItem.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportHtmlItem. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_item_container(self) -> '_1543.CustomReportItemContainer':
        """CustomReportItemContainer: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1543.CustomReportItemContainer.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainer. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_item_container_collection_base(self) -> '_1545.CustomReportItemContainerCollectionBase':
        """CustomReportItemContainerCollectionBase: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1545.CustomReportItemContainerCollectionBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainerCollectionBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_item_container_collection_item(self) -> '_1546.CustomReportItemContainerCollectionItem':
        """CustomReportItemContainerCollectionItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1546.CustomReportItemContainerCollectionItem.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainerCollectionItem. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_multi_property_item_base(self) -> '_1549.CustomReportMultiPropertyItemBase':
        """CustomReportMultiPropertyItemBase: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1549.CustomReportMultiPropertyItemBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportMultiPropertyItemBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_nameable_item(self) -> '_1550.CustomReportNameableItem':
        """CustomReportNameableItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1550.CustomReportNameableItem.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportNameableItem. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_named_item(self) -> '_1551.CustomReportNamedItem':
        """CustomReportNamedItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1551.CustomReportNamedItem.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportNamedItem. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_status_item(self) -> '_1553.CustomReportStatusItem':
        """CustomReportStatusItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1553.CustomReportStatusItem.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportStatusItem. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_tab(self) -> '_1554.CustomReportTab':
        """CustomReportTab: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1554.CustomReportTab.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportTab. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_tabs(self) -> '_1555.CustomReportTabs':
        """CustomReportTabs: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1555.CustomReportTabs.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportTabs. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_report_text(self) -> '_1556.CustomReportText':
        """CustomReportText: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1556.CustomReportText.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportText. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_sub_report(self) -> '_1558.CustomSubReport':
        """CustomSubReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1558.CustomSubReport.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomSubReport. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_table(self) -> '_1559.CustomTable':
        """CustomTable: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1559.CustomTable.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomTable. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_dynamic_custom_report_item(self) -> 'DynamicCustomReportItem':
        """DynamicCustomReportItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if DynamicCustomReportItem.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to DynamicCustomReportItem. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_line_chart(self) -> '_1626.CustomLineChart':
        """CustomLineChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1626.CustomLineChart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomLineChart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_custom_table_and_chart(self) -> '_1627.CustomTableAndChart':
        """CustomTableAndChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1627.CustomTableAndChart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomTableAndChart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_loaded_ball_element_chart_reporter(self) -> '_1709.LoadedBallElementChartReporter':
        """LoadedBallElementChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1709.LoadedBallElementChartReporter.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedBallElementChartReporter. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_loaded_bearing_chart_reporter(self) -> '_1710.LoadedBearingChartReporter':
        """LoadedBearingChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1710.LoadedBearingChartReporter.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedBearingChartReporter. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_loaded_bearing_temperature_chart(self) -> '_1713.LoadedBearingTemperatureChart':
        """LoadedBearingTemperatureChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1713.LoadedBearingTemperatureChart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedBearingTemperatureChart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_loaded_roller_element_chart_reporter(self) -> '_1721.LoadedRollerElementChartReporter':
        """LoadedRollerElementChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _1721.LoadedRollerElementChartReporter.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedRollerElementChartReporter. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_shaft_system_deflection_sections_report(self) -> '_2593.ShaftSystemDeflectionSectionsReport':
        """ShaftSystemDeflectionSectionsReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _2593.ShaftSystemDeflectionSectionsReport.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ShaftSystemDeflectionSectionsReport. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_parametric_study_histogram(self) -> '_4126.ParametricStudyHistogram':
        """ParametricStudyHistogram: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _4126.ParametricStudyHistogram.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ParametricStudyHistogram. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_campbell_diagram_report(self) -> '_4454.CampbellDiagramReport':
        """CampbellDiagramReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _4454.CampbellDiagramReport.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CampbellDiagramReport. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inner_item_of_type_per_mode_results_report(self) -> '_4458.PerModeResultsReport':
        """PerModeResultsReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerItem

        if temp is None:
            return None

        if _4458.PerModeResultsReport.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inner_item to PerModeResultsReport. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
