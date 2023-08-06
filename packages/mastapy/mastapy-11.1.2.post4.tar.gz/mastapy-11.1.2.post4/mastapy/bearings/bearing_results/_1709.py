"""_1709.py

LoadedBallElementChartReporter
"""


from mastapy._internal.implicit import enum_with_selected_value
from mastapy.bearings.bearing_results import _1725
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.utility.report import _1535
from mastapy._internal.python_net import python_net_import

_LOADED_BALL_ELEMENT_CHART_REPORTER = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedBallElementChartReporter')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBallElementChartReporter',)


class LoadedBallElementChartReporter(_1535.CustomReportChart):
    """LoadedBallElementChartReporter

    This is a mastapy class.
    """

    TYPE = _LOADED_BALL_ELEMENT_CHART_REPORTER

    def __init__(self, instance_to_wrap: 'LoadedBallElementChartReporter.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def element_to_plot(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LoadedBallElementPropertyType':
        """enum_with_selected_value.EnumWithSelectedValue_LoadedBallElementPropertyType: 'ElementToPlot' is the original name of this property."""

        temp = self.wrapped.ElementToPlot

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LoadedBallElementPropertyType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @element_to_plot.setter
    def element_to_plot(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LoadedBallElementPropertyType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LoadedBallElementPropertyType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ElementToPlot = value
