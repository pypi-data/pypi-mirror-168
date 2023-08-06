"""_984.py

CylindricalGearMicroGeometrySettings
"""


from mastapy.gears.micro_geometry import _537
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1078
from mastapy.gears.gear_designs.cylindrical import _1005
from mastapy.utility import _1390
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MICRO_GEOMETRY_SETTINGS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearMicroGeometrySettings')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMicroGeometrySettings',)


class CylindricalGearMicroGeometrySettings(_1390.IndependentReportablePropertiesBase['CylindricalGearMicroGeometrySettings']):
    """CylindricalGearMicroGeometrySettings

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MICRO_GEOMETRY_SETTINGS

    def __init__(self, instance_to_wrap: 'CylindricalGearMicroGeometrySettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def flank_side_with_zero_face_width(self) -> '_537.FlankSide':
        """FlankSide: 'FlankSideWithZeroFaceWidth' is the original name of this property."""

        temp = self.wrapped.FlankSideWithZeroFaceWidth

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_537.FlankSide)(value) if value is not None else None

    @flank_side_with_zero_face_width.setter
    def flank_side_with_zero_face_width(self, value: '_537.FlankSide'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FlankSideWithZeroFaceWidth = value

    @property
    def micro_geometry_lead_tolerance_chart_view(self) -> '_1078.MicroGeometryLeadToleranceChartView':
        """MicroGeometryLeadToleranceChartView: 'MicroGeometryLeadToleranceChartView' is the original name of this property."""

        temp = self.wrapped.MicroGeometryLeadToleranceChartView

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1078.MicroGeometryLeadToleranceChartView)(value) if value is not None else None

    @micro_geometry_lead_tolerance_chart_view.setter
    def micro_geometry_lead_tolerance_chart_view(self, value: '_1078.MicroGeometryLeadToleranceChartView'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MicroGeometryLeadToleranceChartView = value

    @property
    def scale_and_range_of_flank_relief_axes_for_micro_geometry_tolerance_charts(self) -> '_1005.DoubleAxisScaleAndRange':
        """DoubleAxisScaleAndRange: 'ScaleAndRangeOfFlankReliefAxesForMicroGeometryToleranceCharts' is the original name of this property."""

        temp = self.wrapped.ScaleAndRangeOfFlankReliefAxesForMicroGeometryToleranceCharts

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1005.DoubleAxisScaleAndRange)(value) if value is not None else None

    @scale_and_range_of_flank_relief_axes_for_micro_geometry_tolerance_charts.setter
    def scale_and_range_of_flank_relief_axes_for_micro_geometry_tolerance_charts(self, value: '_1005.DoubleAxisScaleAndRange'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ScaleAndRangeOfFlankReliefAxesForMicroGeometryToleranceCharts = value
