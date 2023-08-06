"""_614.py

PlungeShaverCalculationInputs
"""


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears import _305
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _698
from mastapy.gears.gear_designs.cylindrical import (
    _1047, _1007, _1027, _1046
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVER_CALCULATION_INPUTS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'PlungeShaverCalculationInputs')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShaverCalculationInputs',)


class PlungeShaverCalculationInputs(_0.APIBase):
    """PlungeShaverCalculationInputs

    This is a mastapy class.
    """

    TYPE = _PLUNGE_SHAVER_CALCULATION_INPUTS

    def __init__(self, instance_to_wrap: 'PlungeShaverCalculationInputs.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def diameter_for_thickness(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DiameterForThickness' is the original name of this property."""

        temp = self.wrapped.DiameterForThickness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @diameter_for_thickness.setter
    def diameter_for_thickness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DiameterForThickness = value

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
    def number_of_teeth_on_the_shaver(self) -> 'int':
        """int: 'NumberOfTeethOnTheShaver' is the original name of this property."""

        temp = self.wrapped.NumberOfTeethOnTheShaver

        if temp is None:
            return None

        return temp

    @number_of_teeth_on_the_shaver.setter
    def number_of_teeth_on_the_shaver(self, value: 'int'):
        self.wrapped.NumberOfTeethOnTheShaver = int(value) if value else 0

    @property
    def shaver_hand(self) -> '_305.Hand':
        """Hand: 'ShaverHand' is the original name of this property."""

        temp = self.wrapped.ShaverHand

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_305.Hand)(value) if value is not None else None

    @shaver_hand.setter
    def shaver_hand(self, value: '_305.Hand'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ShaverHand = value

    @property
    def shaver_helix_angle(self) -> 'float':
        """float: 'ShaverHelixAngle' is the original name of this property."""

        temp = self.wrapped.ShaverHelixAngle

        if temp is None:
            return None

        return temp

    @shaver_helix_angle.setter
    def shaver_helix_angle(self, value: 'float'):
        self.wrapped.ShaverHelixAngle = float(value) if value else 0.0

    @property
    def shaver_normal_module(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ShaverNormalModule' is the original name of this property."""

        temp = self.wrapped.ShaverNormalModule

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @shaver_normal_module.setter
    def shaver_normal_module(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ShaverNormalModule = value

    @property
    def shaver_normal_pressure_angle(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ShaverNormalPressureAngle' is the original name of this property."""

        temp = self.wrapped.ShaverNormalPressureAngle

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @shaver_normal_pressure_angle.setter
    def shaver_normal_pressure_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ShaverNormalPressureAngle = value

    @property
    def shaver_tip_diameter(self) -> 'float':
        """float: 'ShaverTipDiameter' is the original name of this property."""

        temp = self.wrapped.ShaverTipDiameter

        if temp is None:
            return None

        return temp

    @shaver_tip_diameter.setter
    def shaver_tip_diameter(self, value: 'float'):
        self.wrapped.ShaverTipDiameter = float(value) if value else 0.0

    @property
    def thickness_at_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ThicknessAtDiameter' is the original name of this property."""

        temp = self.wrapped.ThicknessAtDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @thickness_at_diameter.setter
    def thickness_at_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ThicknessAtDiameter = value

    @property
    def input_gear_geometry(self) -> '_698.CylindricalCutterSimulatableGear':
        """CylindricalCutterSimulatableGear: 'InputGearGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InputGearGeometry

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tooth_thickness(self) -> '_1047.ToothThicknessSpecificationBase':
        """ToothThicknessSpecificationBase: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThickness

        if temp is None:
            return None

        if _1047.ToothThicknessSpecificationBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness to ToothThicknessSpecificationBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tooth_thickness_of_type_finish_tooth_thickness_design_specification(self) -> '_1007.FinishToothThicknessDesignSpecification':
        """FinishToothThicknessDesignSpecification: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThickness

        if temp is None:
            return None

        if _1007.FinishToothThicknessDesignSpecification.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness to FinishToothThicknessDesignSpecification. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tooth_thickness_of_type_readonly_tooth_thickness_specification(self) -> '_1027.ReadonlyToothThicknessSpecification':
        """ReadonlyToothThicknessSpecification: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThickness

        if temp is None:
            return None

        if _1027.ReadonlyToothThicknessSpecification.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness to ReadonlyToothThicknessSpecification. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tooth_thickness_of_type_tooth_thickness_specification(self) -> '_1046.ToothThicknessSpecification':
        """ToothThicknessSpecification: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThickness

        if temp is None:
            return None

        if _1046.ToothThicknessSpecification.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness to ToothThicknessSpecification. Expected: {}.'.format(temp.__class__.__qualname__))

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
