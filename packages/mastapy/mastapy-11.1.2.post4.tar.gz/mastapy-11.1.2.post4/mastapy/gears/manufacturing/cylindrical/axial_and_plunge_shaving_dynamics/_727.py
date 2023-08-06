"""_727.py

RedressingSettings
"""


from typing import List, Generic, TypeVar

from PIL.Image import Image

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.cutters import _681, _676
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import _731
from mastapy._internal.python_net import python_net_import

_REDRESSING_SETTINGS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'RedressingSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('RedressingSettings',)


T = TypeVar('T', bound='_731.ShavingDynamics')


class RedressingSettings(_0.APIBase, Generic[T]):
    """RedressingSettings

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _REDRESSING_SETTINGS

    def __init__(self, instance_to_wrap: 'RedressingSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def centre_distance(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'CentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CentreDistance

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def icon(self) -> 'Image':
        """Image: 'Icon' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Icon

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

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
    def normal_thickness_at_reference_diameter(self) -> 'float':
        """float: 'NormalThicknessAtReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalThicknessAtReferenceDiameter

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
    def selected(self) -> 'bool':
        """bool: 'Selected' is the original name of this property."""

        temp = self.wrapped.Selected

        if temp is None:
            return None

        return temp

    @selected.setter
    def selected(self, value: 'bool'):
        self.wrapped.Selected = bool(value) if value else False

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
    def shaver_maximum_eap_diameter(self) -> 'float':
        """float: 'ShaverMaximumEAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverMaximumEAPDiameter

        if temp is None:
            return None

        return temp

    @property
    def shaver_minimum_sap_diameter(self) -> 'float':
        """float: 'ShaverMinimumSAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverMinimumSAPDiameter

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
    def shaver_tip_thickness(self) -> 'float':
        """float: 'ShaverTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverTipThickness

        if temp is None:
            return None

        return temp

    @property
    def shaving_status(self) -> 'str':
        """str: 'ShavingStatus' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShavingStatus

        if temp is None:
            return None

        return temp

    @property
    def redressed_shaver(self) -> '_681.CylindricalGearShaver':
        """CylindricalGearShaver: 'RedressedShaver' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RedressedShaver

        if temp is None:
            return None

        if _681.CylindricalGearShaver.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast redressed_shaver to CylindricalGearShaver. Expected: {}.'.format(temp.__class__.__qualname__))

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
