"""_697.py

CutterSimulationCalc
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _698, _703
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _695
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CUTTER_SIMULATION_CALC = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'CutterSimulationCalc')


__docformat__ = 'restructuredtext en'
__all__ = ('CutterSimulationCalc',)


class CutterSimulationCalc(_0.APIBase):
    """CutterSimulationCalc

    This is a mastapy class.
    """

    TYPE = _CUTTER_SIMULATION_CALC

    def __init__(self, instance_to_wrap: 'CutterSimulationCalc.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def base_diameter(self) -> 'float':
        """float: 'BaseDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BaseDiameter

        if temp is None:
            return None

        return temp

    @property
    def base_to_form_radius_clearance(self) -> 'float':
        """float: 'BaseToFormRadiusClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BaseToFormRadiusClearance

        if temp is None:
            return None

        return temp

    @property
    def chamfer_transverse_pressure_angle_at_tip_form_diameter(self) -> 'float':
        """float: 'ChamferTransversePressureAngleAtTipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ChamferTransversePressureAngleAtTipFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def finish_cutter_tip_to_fillet_clearance(self) -> 'float':
        """float: 'FinishCutterTipToFilletClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FinishCutterTipToFilletClearance

        if temp is None:
            return None

        return temp

    @property
    def generating_circle_diameter(self) -> 'float':
        """float: 'GeneratingCircleDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeneratingCircleDiameter

        if temp is None:
            return None

        return temp

    @property
    def lowest_sap_diameter(self) -> 'float':
        """float: 'LowestSAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LowestSAPDiameter

        if temp is None:
            return None

        return temp

    @property
    def maximum_finish_stock_arc_length(self) -> 'float':
        """float: 'MaximumFinishStockArcLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumFinishStockArcLength

        if temp is None:
            return None

        return temp

    @property
    def minimum_finish_stock_arc_length(self) -> 'float':
        """float: 'MinimumFinishStockArcLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumFinishStockArcLength

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def normal_thickness_at_form_diameter(self) -> 'float':
        """float: 'NormalThicknessAtFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalThicknessAtFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def normal_thickness_at_tip_form_diameter(self) -> 'float':
        """float: 'NormalThicknessAtTipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalThicknessAtTipFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def normal_tip_thickness(self) -> 'float':
        """float: 'NormalTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalTipThickness

        if temp is None:
            return None

        return temp

    @property
    def normal_tooth_thickness_on_the_reference_circle(self) -> 'float':
        """float: 'NormalToothThicknessOnTheReferenceCircle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalToothThicknessOnTheReferenceCircle

        if temp is None:
            return None

        return temp

    @property
    def normal_tooth_thickness_on_the_v_circle(self) -> 'float':
        """float: 'NormalToothThicknessOnTheVCircle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalToothThicknessOnTheVCircle

        if temp is None:
            return None

        return temp

    @property
    def profile_shift_coefficient(self) -> 'float':
        """float: 'ProfileShiftCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileShiftCoefficient

        if temp is None:
            return None

        return temp

    @property
    def radial_chamfer_height(self) -> 'float':
        """float: 'RadialChamferHeight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialChamferHeight

        if temp is None:
            return None

        return temp

    @property
    def radial_clearance_between_rough_root_circle_and_theoretical_finish_root_circle(self) -> 'float':
        """float: 'RadialClearanceBetweenRoughRootCircleAndTheoreticalFinishRootCircle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialClearanceBetweenRoughRootCircleAndTheoreticalFinishRootCircle

        if temp is None:
            return None

        return temp

    @property
    def reference_diameter(self) -> 'float':
        """float: 'ReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceDiameter

        if temp is None:
            return None

        return temp

    @property
    def residual_fillet_undercut(self) -> 'float':
        """float: 'ResidualFilletUndercut' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResidualFilletUndercut

        if temp is None:
            return None

        return temp

    @property
    def residual_fillet_undercut_diameter(self) -> 'float':
        """float: 'ResidualFilletUndercutDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResidualFilletUndercutDiameter

        if temp is None:
            return None

        return temp

    @property
    def root_diameter(self) -> 'float':
        """float: 'RootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootDiameter

        if temp is None:
            return None

        return temp

    @property
    def root_form_diameter(self) -> 'float':
        """float: 'RootFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def rough_root_form_diameter(self) -> 'float':
        """float: 'RoughRootFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoughRootFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def sap_to_form_radius_clearance(self) -> 'float':
        """float: 'SAPToFormRadiusClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SAPToFormRadiusClearance

        if temp is None:
            return None

        return temp

    @property
    def theoretical_finish_root_diameter(self) -> 'float':
        """float: 'TheoreticalFinishRootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TheoreticalFinishRootDiameter

        if temp is None:
            return None

        return temp

    @property
    def theoretical_finish_root_form_diameter(self) -> 'float':
        """float: 'TheoreticalFinishRootFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TheoreticalFinishRootFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def tip_diameter(self) -> 'float':
        """float: 'TipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipDiameter

        if temp is None:
            return None

        return temp

    @property
    def tip_form_diameter(self) -> 'float':
        """float: 'TipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def transverse_chamfer_angle_straight_line_approximation(self) -> 'float':
        """float: 'TransverseChamferAngleStraightLineApproximation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseChamferAngleStraightLineApproximation

        if temp is None:
            return None

        return temp

    @property
    def transverse_chamfer_angle_tangent_to_involute_at_tip_form_diameter(self) -> 'float':
        """float: 'TransverseChamferAngleTangentToInvoluteAtTipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseChamferAngleTangentToInvoluteAtTipFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def transverse_root_fillet_radius(self) -> 'float':
        """float: 'TransverseRootFilletRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseRootFilletRadius

        if temp is None:
            return None

        return temp

    @property
    def gear(self) -> '_698.CylindricalCutterSimulatableGear':
        """CylindricalCutterSimulatableGear: 'Gear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gear

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def stock_removed_at_designed_sap(self) -> '_703.FinishStockPoint':
        """FinishStockPoint: 'StockRemovedAtDesignedSAP' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StockRemovedAtDesignedSAP

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def stock_removed_at_reference_diameter(self) -> '_703.FinishStockPoint':
        """FinishStockPoint: 'StockRemovedAtReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StockRemovedAtReferenceDiameter

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def stock_removed_at_rough_tip_form(self) -> '_703.FinishStockPoint':
        """FinishStockPoint: 'StockRemovedAtRoughTipForm' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StockRemovedAtRoughTipForm

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def finish_stock_indexed_arcs(self) -> 'List[_703.FinishStockPoint]':
        """List[FinishStockPoint]: 'FinishStockIndexedArcs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FinishStockIndexedArcs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def gear_fillet_points(self) -> 'List[_695.NamedPoint]':
        """List[NamedPoint]: 'GearFilletPoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearFilletPoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def main_profile_finish_stock(self) -> 'List[_703.FinishStockPoint]':
        """List[FinishStockPoint]: 'MainProfileFinishStock' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MainProfileFinishStock

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
