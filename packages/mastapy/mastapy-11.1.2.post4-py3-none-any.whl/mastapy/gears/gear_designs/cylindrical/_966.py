"""_966.py

CrossedAxisCylindricalGearPair
"""


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _698
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CROSSED_AXIS_CYLINDRICAL_GEAR_PAIR = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CrossedAxisCylindricalGearPair')


__docformat__ = 'restructuredtext en'
__all__ = ('CrossedAxisCylindricalGearPair',)


class CrossedAxisCylindricalGearPair(_0.APIBase):
    """CrossedAxisCylindricalGearPair

    This is a mastapy class.
    """

    TYPE = _CROSSED_AXIS_CYLINDRICAL_GEAR_PAIR

    def __init__(self, instance_to_wrap: 'CrossedAxisCylindricalGearPair.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def centre_distance(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'CentreDistance' is the original name of this property."""

        temp = self.wrapped.CentreDistance

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @centre_distance.setter
    def centre_distance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.CentreDistance = value

    @property
    def contact_ratio(self) -> 'float':
        """float: 'ContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactRatio

        if temp is None:
            return None

        return temp

    @property
    def cutter_normal_pressure_angle(self) -> 'float':
        """float: 'CutterNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterNormalPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def effective_gear_start_of_active_profile_diameter(self) -> 'float':
        """float: 'EffectiveGearStartOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveGearStartOfActiveProfileDiameter

        if temp is None:
            return None

        return temp

    @property
    def gear_end_of_active_profile_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'GearEndOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearEndOfActiveProfileDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def gear_normal_pressure_angle(self) -> 'float':
        """float: 'GearNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearNormalPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def gear_operating_radius(self) -> 'float':
        """float: 'GearOperatingRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearOperatingRadius

        if temp is None:
            return None

        return temp

    @property
    def gear_start_of_active_profile_diameter(self) -> 'float':
        """float: 'GearStartOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearStartOfActiveProfileDiameter

        if temp is None:
            return None

        return temp

    @property
    def operating_normal_pressure_angle(self) -> 'float':
        """float: 'OperatingNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OperatingNormalPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def shaft_angle(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ShaftAngle' is the original name of this property."""

        temp = self.wrapped.ShaftAngle

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @shaft_angle.setter
    def shaft_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ShaftAngle = value

    @property
    def shaver_end_of_active_profile_diameter(self) -> 'float':
        """float: 'ShaverEndOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverEndOfActiveProfileDiameter

        if temp is None:
            return None

        return temp

    @property
    def shaver_operating_radius(self) -> 'float':
        """float: 'ShaverOperatingRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverOperatingRadius

        if temp is None:
            return None

        return temp

    @property
    def shaver_required_end_of_active_profile_diameter(self) -> 'float':
        """float: 'ShaverRequiredEndOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverRequiredEndOfActiveProfileDiameter

        if temp is None:
            return None

        return temp

    @property
    def shaver_start_of_active_profile_diameter(self) -> 'float':
        """float: 'ShaverStartOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverStartOfActiveProfileDiameter

        if temp is None:
            return None

        return temp

    @property
    def shaver_tip_diameter(self) -> 'float':
        """float: 'ShaverTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverTipDiameter

        if temp is None:
            return None

        return temp

    @property
    def shaver_tip_radius(self) -> 'float':
        """float: 'ShaverTipRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverTipRadius

        if temp is None:
            return None

        return temp

    @property
    def shaver_tip_radius_calculated_by_gear_sap(self) -> 'float':
        """float: 'ShaverTipRadiusCalculatedByGearSAP' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverTipRadiusCalculatedByGearSAP

        if temp is None:
            return None

        return temp

    @property
    def shaver(self) -> '_698.CylindricalCutterSimulatableGear':
        """CylindricalCutterSimulatableGear: 'Shaver' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shaver

        if temp is None:
            return None

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
