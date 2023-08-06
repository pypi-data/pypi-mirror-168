"""_732.py

ShavingDynamicsCalculation
"""


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable, list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import _728, _727, _731
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _698
from mastapy.gears.gear_designs.cylindrical import _987
from mastapy.gears.manufacturing.cylindrical.cutters import _681, _676
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAVING_DYNAMICS_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsCalculation',)


T = TypeVar('T', bound='_731.ShavingDynamics')


class ShavingDynamicsCalculation(_0.APIBase, Generic[T]):
    """ShavingDynamicsCalculation

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _SHAVING_DYNAMICS_CALCULATION

    def __init__(self, instance_to_wrap: 'ShavingDynamicsCalculation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def adjusted_tip_diameter(self) -> 'List[float]':
        """List[float]: 'AdjustedTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdjustedTipDiameter

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def life_cutter_normal_thickness(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'LifeCutterNormalThickness' is the original name of this property."""

        temp = self.wrapped.LifeCutterNormalThickness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @life_cutter_normal_thickness.setter
    def life_cutter_normal_thickness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.LifeCutterNormalThickness = value

    @property
    def life_cutter_tip_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'LifeCutterTipDiameter' is the original name of this property."""

        temp = self.wrapped.LifeCutterTipDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @life_cutter_tip_diameter.setter
    def life_cutter_tip_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.LifeCutterTipDiameter = value

    @property
    def new_cutter_tip_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'NewCutterTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NewCutterTipDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def normal_tooth_thickness_reduction_between_redressings(self) -> 'float':
        """float: 'NormalToothThicknessReductionBetweenRedressings' is the original name of this property."""

        temp = self.wrapped.NormalToothThicknessReductionBetweenRedressings

        if temp is None:
            return None

        return temp

    @normal_tooth_thickness_reduction_between_redressings.setter
    def normal_tooth_thickness_reduction_between_redressings(self, value: 'float'):
        self.wrapped.NormalToothThicknessReductionBetweenRedressings = float(value) if value else 0.0

    @property
    def selected_redressing(self) -> 'list_with_selected_item.ListWithSelectedItem_T':
        """list_with_selected_item.ListWithSelectedItem_T: 'SelectedRedressing' is the original name of this property."""

        temp = self.wrapped.SelectedRedressing

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_T)(temp) if temp is not None else None

    @selected_redressing.setter
    def selected_redressing(self, value: 'list_with_selected_item.ListWithSelectedItem_T.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_T.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_T.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.SelectedRedressing = value

    @property
    def accuracy_level_iso6(self) -> '_728.RollAngleRangeRelativeToAccuracy':
        """RollAngleRangeRelativeToAccuracy: 'AccuracyLevelISO6' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyLevelISO6

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_level_iso7(self) -> '_728.RollAngleRangeRelativeToAccuracy':
        """RollAngleRangeRelativeToAccuracy: 'AccuracyLevelISO7' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyLevelISO7

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def designed_gear(self) -> '_698.CylindricalCutterSimulatableGear':
        """CylindricalCutterSimulatableGear: 'DesignedGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DesignedGear

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def life_cutter_start_of_shaving(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'LifeCutterStartOfShaving' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeCutterStartOfShaving

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def life_shaver(self) -> '_681.CylindricalGearShaver':
        """CylindricalGearShaver: 'LifeShaver' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeShaver

        if temp is None:
            return None

        if _681.CylindricalGearShaver.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast life_shaver to CylindricalGearShaver. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def new_cutter_start_of_shaving(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'NewCutterStartOfShaving' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NewCutterStartOfShaving

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaver(self) -> '_681.CylindricalGearShaver':
        """CylindricalGearShaver: 'Shaver' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shaver

        if temp is None:
            return None

        if _681.CylindricalGearShaver.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast shaver to CylindricalGearShaver. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def redressing_settings(self) -> 'List[_727.RedressingSettings[T]]':
        """List[RedressingSettings[T]]: 'RedressingSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RedressingSettings

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

    def cutter_simulation_calculation_required(self):
        """ 'CutterSimulationCalculationRequired' is the original name of this method."""

        self.wrapped.CutterSimulationCalculationRequired()

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
